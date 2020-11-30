"""This module contains the factory function and related helper
functions responsible for instantiating the application.
"""


from flask import Flask
from flask_bcrypt import Bcrypt
from config import CONFIG_MAPPER

# Instantiate extensions
bcrypt = Bcrypt()


def create_app(config_name):
    """Configure and return an instance of the Flask
    application.
    """
    app = Flask(__name__.split(".")[0])
    app.config.from_object(CONFIG_MAPPER[config_name])
    register_extensions(app)
    return app


def register_extensions(app):
    """Register the Flask app with various extensions."""
    bcrypt.init_app(app)