"""This file contains fixtures for running integration tests on all
code that interacts with DynamoDB.
"""


import pytest
from app.dynamodb.mapper import ModelMapper



class FakeModel:
    """Class to be used in serialization and deserialization tests."""

    pass


class FakeMapper(ModelMapper):
    """Class to be used to run tests serializing and deserializing a 
    variety of different types of attributes that could be present on a model.
    """
    pass


@pytest.fixture
def fake_mapper():
    """Return an instance of a FakeMapper."""
    return FakeMapper()


@pytest.fixture
def fake_model:
    """Return an instance of a FakeModel."""
    return FakeModel()