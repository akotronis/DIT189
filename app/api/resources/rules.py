from flask import current_app as app
from flask_smorest import Blueprint


blp = Blueprint("Rules", __name__)

@blp.route('/rules')
def root():
    """
    Returns all api endpoints
    """
    # expose rule, endpoint, methods attributes
    rules = [repr(rules) for rules in app.url_map.iter_rules()]
    return rules