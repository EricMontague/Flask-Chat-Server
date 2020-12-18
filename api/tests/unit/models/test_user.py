"""This file contains tests for the user model."""


import pytest
from app.models import User


def test_read_password_property_raises_error(test_user):
    """Test to confirm that reading the password property
    of a user model raises an error.
    """
    with pytest.raises(AttributeError):
        test_user.password


def test_setting_password_sets_password_hash():
    """Test to confirm that setting the password property
    sets the user's password_hash attribute.
    """
    user = User("qwtqwqwef","coltrane","John","coltrane@gmail.com", None)
    assert user._password_hash is None
    user.password = "Fried fish"
    assert user._password_hash is not None


def test_same_password_generates_different_hash():
    """Test to confirm that two users who have the same
    password are given different password hashes.
    """
    user1 = User("qwtqwqwef","coltrane","John","coltrane@gmail.com", None)
    user2 = User("ewhgwg","miles","Miles Davis","miles@gmail.com", None)
    user1.password = "Cat"
    user2.password = "Cat"
    assert user1._password_hash != user2._password_hash


def test_password_verification(test_user):
    """Test to confirm that a user is propertly verified when providing
    the correct password and denied when they don't.
    """
    test_user.password = "Cat"
    assert test_user.verify_password("Cat") is True
    assert test_user.verify_password("Dog") is False