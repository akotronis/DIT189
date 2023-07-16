from flask import jsonify
from flask_smorest import Blueprint
from flask.views import MethodView

from ..database import DataBase
from ..schemas import RefreshInputSchema, UserSchema


blp = Blueprint("Refresh", __name__)

@blp.route('/refresh')
class Refresh(MethodView):
    @blp.arguments(RefreshInputSchema, location='query')
    @blp.response(200, UserSchema(many=True))
    def get(self, query_args):
        """
        Refresh Database. (No authentication token required)

        Clean all tables and repopulate Users/Marriages.
        - If `drop=True`, drops all tables first and recreate them.
        - If `drop=False`, just returns users.
        """
        drop = query_args.get('drop')
        DataBase.initialize(drop=drop)
        return DataBase.get_users()
        # return jsonify(message='Database Reinitialized'), 200