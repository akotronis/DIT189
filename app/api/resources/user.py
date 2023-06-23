import os
from flask import Flask, g, jsonify, request, redirect
from flask.views import MethodView
from flask_smorest import Blueprint, abort
# from passlib.hash import pbkdf2_sha256
from sqlalchemy.exc import IntegrityError

from ..db import db
from ..models import User
from ..factory import oidc
from ..keycloak import KeycloakAPI
# from schemas import UserSchema


blp = Blueprint('Users', __name__)


@blp.route('/users')
class UserTest(MethodView):
    @oidc.require_login
    def get(self):
        info = oidc.user_getinfo(['preferred_username', 'email', 'sub'])

        username = info.get('preferred_username')
        email = info.get('email')
        user_id = info.get('sub')
        kc = KeycloakAPI()
        kc.delete_user(user_id)
        return {'message': 'Successfully logged out.'}


@blp.route('/users/logout')
class Logout(MethodView):
    @oidc.require_login
    def get(self):
        issuer_url = oidc.client_secrets.get('issuer')
        hosturl = os.getenv('HOST_MAIN_URL')
        oidc.logout()
        return redirect(f'{issuer_url}/protocol/openid-connect/logout?redirect_uri={hosturl}')


@blp.route('/')
class Dum(MethodView):
    def get(self):
        
        return {'message': 'HELLO'}

# @blp.route('/users/register')
# class UserRegister(MethodView):
#     @blp.arguments(UserSchema)
#     def post(self, user_data):
#         user = UserModel(
#                 username=user_data['username'],
#                 password=pbkdf2_sha256.hash(user_data['password'])
#             )
#         db.session.add(user)
#         try:
#             db.session.commit()
#         except IntegrityError:
#             db.session.rollback()
#             abort(400, message='A user with this username already exists')
#         except:
#             db.session.rollback()
#             abort(500, message='Could not register user')
#         return {'message': 'User created succesfully'}, 201


# @blp.route('/users/login')
# class UserLogin(MethodView):
#     @blp.arguments(UserSchema)
#     def post(self, user_data):
#         user = UserModel.query.filter(UserModel.username == user_data['username']).first()
#         if user and pbkdf2_sha256.verify(user_data['password'], user.password):
#             # user.id is stored as value of 'sub' key in JWT payload claims
#             access_token = create_access_token(identity=user.id, fresh=True)
#             return {
#                 'access_token': access_token,
#             }
#         abort(401, message='Invalid credentials')


# @blp.route('/users/logout')
# class UserLogout(MethodView):
#     @jwt_required()
#     def post(self):
#         jti = get_jwt()['jti']
#         BLOCKLIST.add(jti)
#         return {'message': 'Successfully logged out.'}


# @blp.route('/users/<int:user_id>')
# class User(MethodView):

#     @jwt_required()
#     @blp.response(200, UserSchema)
#     def get(self, user_id):
#         if get_jwt()['sub'] != user_id:
#             abort(401, message='User missmatched. Could not get user')
#         user = UserModel.query.get_or_404(user_id)
#         # If we want to make sure we don't send password to Schema in the first place:
#         # user = UserModel.query.with_entities(UserModel.username).filter(UserModel.id==user_id).first()
#         return user

#     @jwt_required()
#     def delete(self, user_id):
#         user = UserModel.query.get_or_404(user_id)
#         if get_jwt()['sub'] != user_id:
#             abort(401, message='User missmatched. Could not delete user')
#         try:
#             db.session.delete(user)
#             db.session.commit()
#         except:
#             db.session.rollback()
#             abort(500, message='Could not delete user')
#         return {'message': 'User deleted succesfully'}, 200