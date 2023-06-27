from .resources.divorce import blp as DivorceBlueprint
from .resources.marriage import blp as MarriageBlueprint
from .resources.user import blp as UserBlueprint

from .resources.rules import blp_rules



def register_blueprints(api):
    api.register_blueprint(blp_rules)
    api.register_blueprint(DivorceBlueprint, url_prefix='/', name='Cases')
    api.register_blueprint(MarriageBlueprint, url_prefix='/', name='Marriages')
    api.register_blueprint(UserBlueprint, url_prefix='/', name='Users')