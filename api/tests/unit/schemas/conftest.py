"""This file contains fixtures for running unit tests
on marshmallow schemas.
"""


import pytest
from app.schemas import (
    UserSchema, 
    LocationSchema, 
    ImageSchema,
    UrlParamsSchema
)
from app.models.user_factory import UserFactory
from .test_data import user_data_dict, user_data_json


@pytest.fixture
def user_schema():
    """Return an instance of a user schema used
    to serialize and deserialize a single
    user model.
    """
    return UserSchema()


@pytest.fixture
def user_schema_many():
    """Return an instance of a user schema used
    to serialize and deserialize a list of
    user models.
    """
    return UserSchema(many=True)


@pytest.fixture
def test_user():
    """Return an instance of a user for tests."""
    return UserFactory.create_user(user_data_dict)


@pytest.fixture
def test_user_json():
    """Return a JSON representation of a user."""
    return user_data_json

