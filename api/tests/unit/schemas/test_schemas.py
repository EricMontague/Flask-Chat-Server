"""This file contains tests for various marshmallow
schemas.
"""


import pytest
from marshmallow import ValidationError


@pytest.mark.parametrize(
    "attribute, value",
    [
        ("username", "Longusername" * 24),
        ("name", ""),
        ("email", "Longemail" * 10 + "@gmail.com"),
        ("bio", "Longbio" * 50),
    ],
)
def test_invalid_length_parameters_raises_error_on_deserialization(
    attribute, value, test_user_dict, user_schema
):
    """Test to confirm that if a field is deserialized with parameters that
    are less than or greater than the valid length, that an error is
    raised.
    """
    test_user_dict[attribute] = value
    with pytest.raises(ValidationError):
        user_schema.load(test_user_dict)


@pytest.mark.parametrize("attribute", ["username", "location", "email"])
def test_missing_required_field_raises_error_on_deserialization(
    attribute, test_user_dict, user_schema
):
    """Test that if a required field is missing on deserialization
    that an error is thrown.
    """
    del test_user_dict[attribute]
    with pytest.raises(ValidationError):
        user_schema.load(test_user_dict)


@pytest.mark.parametrize(
    "field", ["avatar", "cover_photo", "_created_at", "last_seen_at"]
)
def test_unknown_fields_are_excluded_on_deserialization(
    field, test_user_dict, user_schema
):
    """Test that unknown fields are ignored on deserialization."""
    assert field not in user_schema.load(test_user_dict)


def test_unwanted_fields_removed_on_deserialization(test_user_dict, user_schema):
    """Test that unwanted fields defined in the load pre-processor method 
    are not present after deserialization.
    """
    assert "resource_type" not in user_schema.load(test_user_dict)


def test_injected_fields_are_present_on_serialization(test_user_model, user_schema, flask_app):
    """Test that the extra fields added in the dump post-processor
    method are present after serialization.
    """
    user_dict = user_schema.dump(test_user_model)
    assert "is_admin" in user_dict
    assert not user_dict["is_admin"]
