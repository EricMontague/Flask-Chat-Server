"""This file contains fixtures for running unit tests
on marshmallow schemas.
"""


import pytest
from app.schemas import UserSchema, LocationSchema, ImageSchema, UrlParamsSchema
from app.models.user_factory import UserFactory
from test_data import partial_user_data, complete_user_data


@pytest.fixture
def user_schema():
    """Return an instance of a user schema used
    to serialize and deserialize a single
    user model.
    """
    return UserSchema(partial=["password"])


@pytest.fixture
def test_user_model():
    """Return an instance of a user for tests."""
    return UserFactory.create_user(partial_user_data)


@pytest.fixture
def test_user_dict():
    """Return a deserialized representation of a user."""
    return complete_user_data.copy()

