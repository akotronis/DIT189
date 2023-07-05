from flask import jsonify
from flask_smorest import Blueprint
from flask.views import MethodView

from ..database import DataBase
from ..schemas import RefreshInputSchema


blp = Blueprint("Refresh", __name__)

@blp.route('/refresh')
class Refresh(MethodView):
    @blp.arguments(RefreshInputSchema, location='query')
    def get(self, query_args):
        """
        Refresh Database. (No authentication token required)

        Clean all tables and repopulate Users/Marriages.
        If `drop=True`, drops all tables first and recreate them.
        """
        drop = query_args.get('drop')
        DataBase.initialize(fresh=True, drop=drop)
        return jsonify(message='Database Reinitialized'), 200