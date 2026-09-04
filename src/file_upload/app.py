from flask import Flask
from .config import Config
from .extensions import jwt
from .routes.auth import auth_blueprint
from .routes.tasks import task_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    jwt.init_app(app)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(task_bp)
    return app


app = create_app()
