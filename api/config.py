"""This file contains the configuration classes for the application."""


import os


PROJECT_ROOT_DIRECTORY = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    """Base configuration class for the application."""

    # Make sure this is set for production
    SECRET_KEY = os.environ.get("SECRET_KEY", "hard to guess string")
    RESULTS_PER_PAGE = 20
    ALLOWED_FILE_EXTENSIONS = {"png", "jpg", "jpeg"}
    MAX_CONTENT_LENGTH = 1024 * 1024


class DevelopmentConfig(BaseConfig):
    """Class to be used for configuring the application in
    development.
    """

    DEBUG = True


class TestingConfig(BaseConfig):
    """Class to be used for configuring the application in
    testing.
    """

    TESTING = True


class ProductionConfig(BaseConfig):
    """Class to be used for configuring the application in
    production.
    """

    pass


CONFIG_MAPPER = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}
