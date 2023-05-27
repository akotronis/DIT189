import os
from factory import create_app


if __name__ == "__main__":
    app = create_app(os.getenv('WORK_ENV') or 'dev')
    app.run(host='0.0.0.0')