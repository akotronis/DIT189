import os
from flask_smorest import Api
from .versioning import register_blueprints
from .factory import create_app

# Create app
app = create_app(os.getenv('WORK_ENV') or 'dev')

# Connect flask_smorest to the app
api = Api(app)

# Register Blueprints
register_blueprints(api)