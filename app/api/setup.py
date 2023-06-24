import os

from .factory import create_app


# Create app
app = create_app(os.getenv('WORK_ENV') or 'dev')