import os
from flask import Flask, g, jsonify, request, redirect
from flask.views import MethodView
from flask_smorest import Blueprint, abort
# from passlib.hash import pbkdf2_sha256
from sqlalchemy.exc import IntegrityError

from ..database import DataBase
from ..keycloak import KeycloakAPI
from ..schemas import MarriageInputSchema, MarriageUserDivorceSchema


blp = Blueprint('Marriages', __name__)
kclk = KeycloakAPI()


@blp.route('/marriages')
class MarriageList(MethodView):
    # @kclk.token_required()
    @blp.arguments(MarriageInputSchema, location='query')
    @blp.response(200, MarriageUserDivorceSchema(many=True))
    def get(self, query_args):
        """
        Accepts query params:
            optional in_use=True/False to select based on Marriage.in_use
        """
        
        in_use = query_args.get('in_use', {})
        marriages = DataBase.get_marriages(**in_use).all()
        return marriages    