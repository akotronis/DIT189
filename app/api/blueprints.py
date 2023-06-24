from .resources.user import blp as UserBlueprint

from .resources.rules import blp_rules



def register_blueprints(api):
    api.register_blueprint(blp_rules)

    api.register_blueprint(UserBlueprint, url_prefix='/', name='Users')