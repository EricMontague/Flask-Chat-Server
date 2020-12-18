"""This file contains tests for various marshmallow
schemas.
"""


import pytest
import json
from marshmallow import ValidationError


@pytest.mark.parametrize(
    "attribute", "value",
    [
        ("username", "Longusername" * 24), 
        ("name", ""), 
        ("email", "Longemail" + 10 + "@gmail.com"),
        ("bio", "Longbio" * 50)
    ]
)
def test_deserialize_invalid_length_parameters_raises_error(attribute, value, test_user_dict, user_schema):
    """Test to confirm that if a field is deserialized with parameters that
    are less than or greater than the valid length, that an error is
    raised.
    """
    test_user_dict[attribute] = value
    json_user_data = json.dumps(test_user_dict)
    with pytest.raises(ValidationError):
        user_schema.load(json_user_data)



@pytest.mark.parametrize("attribute", ["username", "location", "email"])
def test_deserialize_missing_required_field_raises_error(attribute, test_user_dict, user_schema):
    """Test that if a required field is missing on deserialization
    that an error is thrown.
    """
    del test_user_dict[attribute]
    json_user_data = json.dumps(test_user_dict)
    with pytest.raises(ValidationError):
        user_schema.load(json_user_data)


@pytest.mark.parametrize(
    "field", 
    ["avatar", "cover_photo", "_created_at", "last_seen_at"]
)
def test_deserialize_unknown_fields_are_excluded(field, test_user_dict, user_schema):
    """Test that unknown fields are ignored on deserialization."""
    json_user_data = json.dumps(test_user_dict)
    deserialized_user_data = user_schema.load(json_user_data)
    assert field not in deserialized_user_data


def test_deserialize_unwanted_fields_removed(test_user_dict, user_schema):
    """Test that unwanted fields defined in the pre load processor method 
    are not present after deserialization.
    """
    json_user_data = json.dumps(test_user_dict)
    deserialized_user_data = user_schema.load(json_user_data)
    assert "resource_type" not in deserialized_user_data


def test_deserialize_uuid_converted_to_hex():
    pass


def test_serialize_injected_fields_are_present():
    pass