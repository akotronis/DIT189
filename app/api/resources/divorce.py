from datetime import datetime
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from ..database import DataBase
from ..models import Divorce, User, UsersDivorces
from ..keycloak import KeycloakAPI
from ..schemas import DivorceCreateSchema, DivorceInputSchema, DivorceInputUpdateSchema, DivorceSchema, DivorceUpdateSchema


blp = Blueprint('Case', __name__)
kclk = KeycloakAPI()


@blp.route('/cases')
class DivorceList(MethodView):
    @kclk.token_required()
    @blp.arguments(DivorceInputSchema, location='query')
    @blp.response(200, DivorceSchema(many=True))
    def get(self, query_args):
        """
        Get all cases (divorces) (Requires authentication token)

        Accepts query params:
        - Multiple of type `&status=COMPLETED&status=CANCELLED` etc (Optional)<br>
        - `self=True/False` to return only divorces (cases) wher user is involved
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
        """
        Create a case (divorce) (Requires authentication token of role lawyer)

        Accepts json with the ids of **marriage**, **notary** and **other lawyer** ids
        """

        # Get lawyer email
        lawyer_email = kclk.token_info.get('email')
        
        # Get marriage info
        marriage_id = divorce_data.get('marriage_id')
        marriage_dict = {'id': marriage_id}
        marriage = DataBase.get_marriages(**marriage_dict).first()

        # if marriage is not found return error
        if not marriage:
            abort(400, message="Marriage not found.")

        # if marriage is not in use return error
        marriage_not_in_use = not marriage.in_use
        if marriage_not_in_use:
            abort(400, message="Marriage not in use.")
        
        # Get notary info
        notary_id = divorce_data.get('notary_id')
        notary_dict = {'id': notary_id, 'role':User.Types.NOTARY}
        notary = DataBase.get_users(**notary_dict).first()

        # if notary is not found return error
        if not notary:
            abort(400, message="Notary not found.")
        
        # Get other lawyer info
        other_lawyer_id = divorce_data.get('other_lawyer_id')
        other_lawyer_dict = {'id': other_lawyer_id, 'role':User.Types.LAWYER}
        other_lawyer = DataBase.get_users(**other_lawyer_dict).first()
        
        # if other lawyer is not found or same as first return error
        if not other_lawyer or other_lawyer.email == lawyer_email:
            abort(400, message="Other laywer not found.")

        # Make marriage not in use for as long a divorce status is not cancelled
        DataBase.update_marriages(marriage_dict, {'in_use': False})
        
        # Start divorce
        divorce = DataBase.start_divorce(marriage, lawyer_email, other_lawyer, notary)
        return divorce, 201
    

@blp.route('/cases/<uuid:case_id>')
class DivorceDetail(MethodView):
    @kclk.token_required()
    @blp.arguments(DivorceInputUpdateSchema, location='query')
    @blp.arguments(DivorceUpdateSchema)
    @blp.response(201, DivorceSchema)
    def put(self, query_args, divorce_data, case_id):
        """
        Update a case (divorce) (Requires authentication token)

        Accepts query params:
        - `?confirm=True/False` to declare confirmation or cancelling from the loggedin user
    
        """
        divorce_id = case_id
        # Fetch divorce and if already cancelled/completed, abort
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

        # Determine new status
        new_status = None
        # User wants to cancel
        if not confirm:
            # If can't cancel abort
            if not DataBase.user_can_cancel(existing_divorce, user):
                abort(400, "Cannot cancel divorce. Over 10 days since start.")
            new_status = Divorce.Status.CANCELLED
        # User wants to confirm
        else:
            # If can't confirm abort
            if not DataBase.user_can_confirm(existing_divorce, user):
                abort(400, "Cannot confirm divorce.")
            new_status = DataBase.confirmed_divorce_new_status(existing_divorce, user)

        # If status is None, abort
        if not new_status:
            abort(400, message="Can't confirm divorce. Wait for other roles first or case closed")
        
        # If new status is WAIT_10DAYS, update divorce_data with start_10day_date
        if new_status.name == Divorce.Status.WAIT_10DAYS.name:
            divorce_data['start_10day_date'] = datetime.now().date()

        # If divorce is completed, update divorce_data with end_date
        if new_status.name == Divorce.Status.COMPLETED.name:
            divorce_data['end_date'] = datetime.now().date()

        cancelled_by = user_id if not confirm else None

        # Update data with query param and id from url
        divorce_data['id'] = divorce_id
        divorce_data['confirm'] = confirm
        divorce_data['cancelled_by'] = cancelled_by
        divorce_data['status'] = new_status
        
        # Check valid combinations of new status values and other incoming data
        agreement_text = divorce_data.get('agreement_text')
        status_completed = new_status.name == Divorce.Status.COMPLETED.name
        if status_completed and not agreement_text:
            abort(400, message="Completed status with missing agreement_text")

        # Update and return divorce
        updated_divorce = DataBase.update_divorce(**divorce_data)
        
        status_cancelled = new_status.name == Divorce.Status.CANCELLED.name
        if not status_cancelled:
            # Update UsersDivorces
            divorce_user_role = user_role
            if divorce_user_role == User.Types.LAWYER.name:
                divorce_user_role = UsersDivorces.UserRole.SECONDARY_LAWYER.name
            DataBase.add_users_divorces(user_id=user_id, divorce_id=existing_divorce.id, user_role=divorce_user_role, confirmed=True)
        
        # Update marriage
        marriage = existing_divorce.marriage
        marriage_id_dict = {'id':marriage.id}
        if status_completed:
            DataBase.update_marriages(marriage_id_dict, {'end_date':datetime.now().date()})
        if status_cancelled:
            DataBase.update_marriages(marriage_id_dict, {'in_use':True})
        return updated_divorce, 200