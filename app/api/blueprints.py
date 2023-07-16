from .resources.divorce import blp as DivorceBlueprint
from .resources.marriage import blp as MarriageBlueprint
from .resources.user import blp as UserBlueprint

from .resources.refresh import blp as RefreshBlueprint
from .resources.rules import blp as RulesBlueprint



def register_blueprints(api):
    api.register_blueprint(RulesBlueprint)
    api.register_blueprint(RefreshBlueprint)
    api.register_blueprint(DivorceBlueprint, url_prefix='/', name='Cases')
    api.register_blueprint(MarriageBlueprint, url_prefix='/', name='Marriages')
    api.register_blueprint(UserBlueprint, url_prefix='/', name='Users')