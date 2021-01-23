"""This file contains fixtures for running tests on models."""


import pytest
from app.models.factories import UserFactory


@pytest.fixture
def test_user():
    """Return an instance of a user for tests."""
    user_data = {
        "name": "Brad",
        "username": "brad345",
        "email": "brad@gmail.com",
        "password": "facebook",
        "location": {
            "city": "Philadelphia",
            "state": "Pennsylvania",
            "country": "United States"
        }
    }
    return UserFactory.create_user(user_data)

