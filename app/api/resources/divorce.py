import os
from flask import Flask, g, jsonify, request, redirect
from flask.views import MethodView
from flask_smorest import Blueprint, abort
# from passlib.hash import pbkdf2_sha256
from sqlalchemy.exc import IntegrityError

from ..database import DataBase
from ..keycloak import KeycloakAPI
from ..schemas import DivorceCreateSchema, DivorceInputSchema, DivorceSchema


blp = Blueprint('Case', __name__)
kclk = KeycloakAPI()


@blp.route('/cases')
class DivorceList(MethodView):
    @kclk.token_required()
    @blp.arguments(DivorceInputSchema, location='query')
    @blp.response(200, DivorceSchema(many=True))
    def get(self, query_args):
        """
        Accepts query params:
            optional multiple key:value of type &status=COMPLETED&role=CANCELLED etc
            optional self=True/False to return only divorces(cases)
        """
        
        status = query_args.get('status', [])
        divorces = DataBase.get_divorces(status=status).all()
        print(divorces)
        self_ = query_args.get('self', None)
        if self_ == True:
            email = kclk.token_info.get('email')
            divorces = [divorce for divorce in divorces if email in [user.email for user in divorce.users]]
        return divorces
    
    @kclk.token_required()
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

        print(' HERE 1 '.center(80, '='))
        # Make marriage not in use for as long a divorce status is not cancelled
        DataBase.update_marriages(marriage_dict, {'in_use': False})
        
        # Get lawyer email and start divorce
        lawyer_email = kclk.token_info.get('email')
        divorce = DataBase.start_divorce(marriage, lawyer_email)

        
        divorce_id = divorce.id
        return divorce, 201