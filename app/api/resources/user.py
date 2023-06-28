import os
from flask import Flask, g, jsonify, request, redirect
from flask.views import MethodView
from flask_smorest import Blueprint, abort
# from passlib.hash import pbkdf2_sha256
from sqlalchemy.exc import IntegrityError

from ..database import DataBase
from ..keycloak import KeycloakAPI
from ..schemas import UserInputSchema, UserSchema


blp = Blueprint('Users', __name__)
kclk = KeycloakAPI()


@blp.route('/users')
class UserList(MethodView):
    # @kclk.token_required('NOTARY')
    # @kclk.token_required(['notary', 'lawyer'])
    @kclk.token_required()
    @blp.arguments(UserInputSchema, location='query')
    @blp.response(200, UserSchema(many=True))
    def get(self, query_args):
        """
        Accepts query params:
            optional multiple key:value of type &role=SPOUSE&role=LAWYER etc
            optional self=True/False to include self or not
        """
        # Can also fetch by request.args.to_dict(flat=False).get('role', [])
        # but it won't be deserialized/validated
        role = query_args.get('role', [])
        users = DataBase.get_users(role=role)
        self_ = query_args.get('self', None)
        if self_ == False:
            email = kclk.token_info.get('email')
            users = [user for user in users if not user.email == email]
        return users