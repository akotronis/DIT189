import os
from flask import Flask, g, jsonify, request, redirect
from flask.views import MethodView
from flask_smorest import Blueprint, abort
# from passlib.hash import pbkdf2_sha256
from sqlalchemy.exc import IntegrityError

from ..database import DataBase
from ..models import Divorce, User
from ..keycloak import KeycloakAPI
from ..schemas import DivorceCreateSchema, DivorceInputSchema, DivorceInputUpdateSchema, DivorceSchema, DivorceUpdateSchema


blp = Blueprint('Case', __name__)
kclk = KeycloakAPI()


@blp.route('/cases')
class DivorceList(MethodView):
    # @kclk.token_required()
    @blp.arguments(DivorceInputSchema, location='query')
    @blp.response(200, DivorceSchema(many=True))
    def get(self, query_args):
        """
        Accepts query params:
            optional multiple key:value of type &status=COMPLETED&role=CANCELLED etc
            optional self=True/False to return only divorces(cases) wher user is involved
        """
        
        status = query_args.get('status', [])
        divorces = DataBase.get_divorces(status=status).all()
        self_ = query_args.get('self', None)
        if self_ == True:
            email = kclk.token_info.get('email')
            divorces = [divorce for divorce in divorces if email in [user.email for user in divorce.users]]
        return divorces
    
    @kclk.token_required('lawyer')
    @blp.arguments(DivorceCreateSchema)
    @blp.response(201, DivorceSchema)
    def post(self, divorce_data):
        
        # Get marriage info
        marriage_id = divorce_data.get('marriage_id')
        marriage_dict = {'id': marriage_id}
        marriage = DataBase.get_marriages(**marriage_dict).first()

        # if marriage is not in use return error
        marriage_not_in_use = not marriage.in_use
        if marriage_not_in_use:
            abort(400, message="Marriage not in use.")

        # Make marriage not in use for as long a divorce status is not cancelled
        DataBase.update_marriages(marriage_dict, {'in_use': False})
        
        # Get lawyer email and start divorce
        lawyer_email = kclk.token_info.get('email')
        divorce = DataBase.start_divorce(marriage, lawyer_email)
        return divorce, 201
    

@blp.route('/cases/<uuid:divorce_id>')
class DivorceDetail(MethodView):
    @kclk.token_required()
    @blp.arguments(DivorceInputUpdateSchema, location='query')
    @blp.arguments(DivorceUpdateSchema)
    @blp.response(201, DivorceSchema)
    def put(self, query_args, divorce_data, divorce_id):
        # Fetch divorce and if allready cancelled, abort
        existing_divorce = Divorce.query.get_or_404(divorce_id)
        existing_divorce_status = existing_divorce.status.name
        if existing_divorce_status == Divorce.Status.CANCELLED.name:
            abort(400, message="This Divorce is already cancelled")
        if existing_divorce_status == Divorce.Status.COMPLETED.name:
            abort(400, message="This Divorce is already completed")

        # Boolean value: confirmation/rejection from logged in user
        confirm = query_args.get('confirm')

        # Fetch logged in user
        email = kclk.token_info.get('email')
        user = DataBase.get_users(email=email).first()
        user_id, user_role = user.id, user.role.name

        time_elapsed = DataBase.time_elapsed_from_divorce_creation(existing_divorce)

        # Determine new status
        new_status = None
        # User wants to cancel
        if not confirm:
            # If user is not Notary and passed over 10 days abort
            if all([
                user_role != User.Types.NOTARY.name,
                time_elapsed > 10
            ]):
                abort(400, "Cannot cancel divorce. Over 10 days since start.")
            new_status = Divorce.Status.CANCELLED
        # User wants to confirm
        else:
            new_status = DataBase.divorce_status_from_confirmations(existing_divorce, user)

        cancelled_by = user_id if not confirm else None

        # Update data with query param and id from url
        divorce_data['confirm'] = confirm
        divorce_data['id'] = divorce_id
        divorce_data['cancelled_by'] = cancelled_by
        divorce_data['status'] = new_status
        
        
        
        


        # Check valid combinations of new status values and other incoming data
        end_date = divorce_data.get('end_date')
        agreement_text = divorce_data.get('agreement_text')
        status_cancelled = new_status.name == Divorce.Status.CANCELLED.name
        status_completed = new_status.name == Divorce.Status.COMPLETED.name
        if status_completed and not agreement_text:
            abort(400, message="Completed status with missing agreement_text")
        if any([status_cancelled, status_completed]) and not end_date:
            abort(400, message="Cancelled/Completed status with missing end_date")

        # Update and return divorce
        updated_divorce = DataBase.update_divorce(**divorce_data)
        return updated_divorce, 200