from flask.views import MethodView
from flask_smorest import Blueprint, abort

from ..database import DataBase
from ..keycloak import KeycloakAPI
from ..schemas import MarriageInputSchema, MarriageUserDivorceSchema


blp = Blueprint('Marriages', __name__)
kclk = KeycloakAPI()


@blp.route('/marriages')
class MarriageList(MethodView):
    @kclk.token_required()
    @blp.arguments(MarriageInputSchema, location='query')
    @blp.response(200, MarriageUserDivorceSchema(many=True))
    def get(self, query_args):
        """
        Get all marriages (Requires authentication token)

        Accepts query params:
        - `in_use=True/False` to filter based on whether a Marriage is in_use or not. If `None`, return all
        """
        
        in_use = query_args.get('in_use', None)
        in_use =  {'in_use': in_use} if in_use is not None else {}
        marriages = DataBase.get_marriages(**in_use).all()
        return marriages    