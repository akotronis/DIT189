import os
from flask import Flask, g, jsonify, request, redirect
from flask.views import MethodView
from flask_smorest import Blueprint, abort
# from passlib.hash import pbkdf2_sha256
from sqlalchemy.exc import IntegrityError

from ..database import DataBase
from ..keycloak import KeycloakAPI
from ..schemas import DivorceInputSchema, DivorceSchema


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
        """
        
        status = query_args.get('status', [])
        divorces = DataBase.get_divorces(status=status)
        return divorces 