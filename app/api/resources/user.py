from flask import jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from ..database import DataBase
from ..keycloak import KeycloakAPI
from ..schemas import KeycloakUserInputSchema, KeycloakUserOutputSchema, UserInputSchema, UserSchema


blp = Blueprint('Users', __name__)
kclk = KeycloakAPI()


@blp.route('/users')
class UserList(MethodView):
    # Leave it WITHOUT token to get users from swagger and see emails/usernames/roles
    # @kclk.token_required()
    @blp.arguments(UserInputSchema, location='query')
    @blp.response(200, UserSchema(many=True))
    def get(self, query_args):
        """
        Get all users (No authentication token required)

        Accepts query params:
        - Multiple of type `&role=SPOUSE&role=LAWYER` etc to filter based on user roles
        - `self=True/False` to include self or not
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
    
    @blp.arguments(KeycloakUserInputSchema, location='query')
    @blp.response(200, KeycloakUserOutputSchema)
    @blp.alt_response(404, description="Can't create user of requested role")
    def post(self, query_args):
        """
        Create a user with a specific role in Keycloak (No authentication token required)

        Selects a user of the given role from api db and creates
        in keycloak a user with this role and password 'pasword'.<br>
        Returns email and Keycloak token<br><br>

        Accepts query params:
        - ?role=LAWYER/SPOUSE etc single.        
        """
        kclk_users = kclk.get_users()
        role = query_args.get('role')
        kclk_user_emails = [user.get('email') for user in kclk_users]
        api_users = DataBase.get_users(role=role).all()
        api_users_not_in_klck = [user for user in api_users if user.email not in kclk_user_emails]
        user_to_create = next(iter(api_users_not_in_klck), None)
        if not user_to_create:
            abort(404, message="Can't create user of requested role")
        email = user_to_create.email
        password = 'password'
        user_data = {
            'email': email,
            'username': user_to_create.username,
            'password': password,
            'enabled': True,
            'firstName': user_to_create.first_name,
            'lastName': user_to_create.last_name,
        }
        kclk.create_user(user_data)
        token = kclk.get_token_from_credentials(email, password).get('access_token')
        return jsonify(email=email, token=token), 201