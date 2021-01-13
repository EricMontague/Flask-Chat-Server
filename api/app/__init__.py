"""This module contains the factory function and related helper
functions responsible for instantiating the application.
"""


from flask import Flask
from app.extensions import bcrypt, ma, socketio
from app.api import api as api_blueprint
from app.auth import auth as auth_blueprint
from app.sockets import sockets as sockets_blueprint
from config import CONFIG_MAPPER


def create_app(config_name):
    """Configure and return an instance of the Flask
    application.
    """
    app = Flask(__name__.split(".")[0])
    app.config.from_object(CONFIG_MAPPER[config_name])
    register_extensions(app)
    register_blueprints(app)
    return app


def register_extensions(app):
    """Register the Flask app with various extensions."""
    bcrypt.init_app(app)
    ma.init_app(app)
    socketio.init_app(app)
    

def register_blueprints(app):
    """Register blueprints with the Flask app."""
    app.register_blueprint(api_blueprint, url_prefix="/api/v1")
    app.register_blueprint(auth_blueprint, url_prefix="/auth")
    app.register_blueprint(sockets_blueprint)
