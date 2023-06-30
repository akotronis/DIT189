from functools import wraps
import os
from flask import request
from flask_smorest import abort
from keycloak import KeycloakAdmin, KeycloakOpenID, KeycloakOpenIDConnection
# import requests

from .database import DataBase


class KeycloakAPI:
    def __init__(self):
        self.url = os.getenv('KEYCLOAK_URI')
        #### jboss image ###
        self.auth_url = f'{self.url}/auth/'
        ### quay.io image ###
        # self.auth_url = self.url
        self.master_realm = os.getenv('ADMIN_REALM')
        self.realm = os.getenv('REALM')
        self.admin_client_id = os.getenv('ADMIN_CLIENT_ID')
        self.client_id = os.getenv('CLIENT_ID')
        self.client_secret = os.getenv('CLIENT_SECRET')
        self.admin_username = os.getenv('KEYCLOACK_ADMIN')
        self.admin_password = os.getenv('KEYCLOACK_PASSWORD')

        ### Object to handle token/user info ###
        self.openid = KeycloakOpenID(
            realm_name=self.realm,
            client_id=self.client_id,
            client_secret_key=self.client_secret,
            server_url=self.auth_url
        )
        self.public_key = self.get_public_key()

        self.conn = KeycloakOpenIDConnection(
            server_url=self.auth_url,
            username=self.admin_username,
            password=self.admin_password
        )
        ### Object to perform keycloak admin actions ###
        self.admin = KeycloakAdmin(connection=self.conn)
        self.change_realm(self.realm)

        # This will store daat from the decoded token, if decoding is successful
        self.token_info = {}

    def get_token_from_credentials(self, username, password, key=None):
        try:
            token = self.openid.token(username, password)
            return token.get(key) if key else token
        except:
            return {}

    def get_public_key(self):
        try:
            return f'-----BEGIN PUBLIC KEY-----\n{self.openid.public_key()}\n-----END PUBLIC KEY-----'
        except Exception as e:
            if 'Realm does not exist' in str(e):
                pass

    def decode_token(self, token):
        """
        Decode and validate token. Used in Authentication
        """
        options = {
            # Check 'Protocol Mappers'
            # https://www.keycloak.org/docs/latest/server_admin/#_audience_hardcoded
            # https://github.com/marcospereirampj/python-keycloak/issues/89#issuecomment-661071539
            'verify_aud':False,
            'verify_exp':True,
            'verify_signature':True
        }
        self.token_info = self.openid.decode_token(token, key=self.public_key, options=options) or {}
        return self.token_info

    def change_realm(self, new_realm):
        self.conn.realm_name = new_realm

    def get_user_by_id(self, user_id):
        return self.admin.get_user(user_id)
    
    def get_user_by_username(self, username):
        user_id = self.admin.get_user_id(username)
        return self.get_user_by_id(user_id)
    
    def get_user_by_email(self, email):
        """
        Email is unique, so we return first user or {} out of an 
        empty list, or list of a unique user.
        User data will be a dictionary
        """
        return next(iter(self.admin.get_users({'email':email})), {})

    def create_user(self, user_data):
        """
        user_data = {'email': email,
                    'username': username,
                    'firstName': first_name,
                    'lastName': last_name,
                    'enabled': enabled,
                    'password': password}
        """
        if 'password' in user_data:
            password = user_data.pop('password')
            user_data['credentials'] = [{'type': 'password', 'value': password}]
        # Raise exception if `username` or `email` exist in realm
        user = self.admin.create_user(user_data, exist_ok=False)
        return user
    
    def update_user(self, username=None, user_id=None, user_data=None):
        """
        In order to be able to change the username in keycloak, we must set
        Edit username: ON on Login tab of Realm Settings
        user_data format as in `create_user`
        """
        user_data = user_data or {}
        if 'password' in user_data:
            password = user_data.pop('password')
            user_data['credentials'] = [{'type': 'password', 'value': password}]
        user_id = self.admin.get_user_id(username) if username else user_id
        self.admin.update_user(user_id=user_id, payload=user_data)
        user = self.get_user_by_id(user_id)
        return user
    
    def delete_user(self, username=None, user_id=None, deactivate=False):
        """
        If `deactivate=True` then deactivate user in keycloak, else delete
        """
        user_id = self.admin.get_user_id(username) if username else user_id
        if deactivate:
            data = {'enabled':False}
            return self.update_user(user_id=user_id, user_data=data)
        self.admin.delete_user(user_id=user_id)

    def token_required(self, roles=None):
        """
        Authenticate based on Keycloak token. If role is provided,
        apply authorization based on role
        """
        def decorator(func_to_decorate):
            """
            Decorator to use in endpoints to handle keycloak authentication
            """
            # Used to keep decorated function's metadata after decorating it,
            # like __name__, __doc__
            @wraps(func_to_decorate)
            def decorated_func(*args, **kwargs):
                auth_header = request.headers.get('Authorization', '')
                error_data = {
                    'http_status_code': 401,
                    'message': 'HTTP 401 Unauthenticated',
                    'headers': {'WWW-Authenticate': 'Bearer'}
                }
                auth = auth_header.split()
                if len(auth) != 2 or not next(iter(auth), None) == 'Bearer':
                    error_data['message'] = 'Invalid token header. Check token header format.'
                    abort(**error_data)
                try:
                    token = auth[1]
                    self.decode_token(token)
                except Exception as e:
                    error_data['message'] = str(e)
                    abort(**error_data)
                # If got here, token is successfully authenticated
                username=self.token_info.get('preferred_username')
                # Fetch user from api database
                user = DataBase.get_users(username=username).first()
                # If not found
                if user is None:
                    # Delete user from keycloak
                    self.delete_user(username)
                    abort(**{'http_status_code': 404, 'message': 'User not found'})
                # User is found in api database.
                # Verify authorization if endpont is authorized based on role
                if roles:
                    if isinstance(roles, list):
                        _roles = [role.upper() for role in roles]
                    elif isinstance(roles, str):
                        _roles = [roles.upper()]
                    if user.role.name not in _roles:
                        error_data = {
                            'http_status_code': 403,
                            'message': 'HTTP 403 Unauthorized'
                        }
                        abort(**error_data)
                return func_to_decorate(*args, **kwargs)
            return decorated_func
        return decorator