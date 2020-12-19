"""This file contains fixtures to be used in tests for the helper functions."""


import pytest
from marshmallow import ValidationError


class FakeValidationError(ValidationError):

    def __init__(self, message, field_name):
        self.message = message
        super().__init__(self.message)
        self.messages = {field_name: self.message}


class FakeErrorSchema:
    """Fake marshmallow schema whose methods raise ValidationErrors."""

    def __init__(self, field_name="_schema"):
        self.validation_error = FakeValidationError("Error successfully raised", field_name)

    def load(self, data):
        raise self.validation_error
       
    def dump(self, model):
        raise self.validation_error


class FakeDataSchema:
    """Fake marshmallow schema whose methods return dictionaries."""

    def __init__(self):
        self.user_data = {
            "id": 2,
            "username": "Brad12",
            "password": "test_password",
            "location": {
                "state": "New York",
                "city": "New York",
                "country": "US"
            }
        }

    def load(self, data):
        return data

    def dump(self, model):
        return self.user_data


@pytest.fixture
def fake_error_schema_class():
    """Return a fake marshmallow schema that only throws errors"""
    return FakeErrorSchema


@pytest.fixture
def fake_data_schema():
    """Return a fakem marshmallow schema whose methods returns data."""
    return FakeDataSchema()

