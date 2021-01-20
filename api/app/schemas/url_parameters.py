"""This module contains the schema for serializing and deserializing
information from url parameters
"""


import uuid
from app.extensions import ma
from app.schemas.enum_field import EnumField
from app.schemas.location import LocationSchema
from app.models import CommunityTopic
from marshmallow import EXCLUDE, validates_schema, ValidationError, validate, post_load


class UrlParamsSchema(ma.Schema):
    """Class to parse and validate information from url parameters"""

    class Meta:
        unknown = EXCLUDE

    per_page = ma.Integer()
    next_cursor = ma.Str(data_key="next")


class GroupChatUrlParamsSchema(UrlParamsSchema):
    """Class to parse and validate information from Group Chat url parameters."""

    class Meta:
        unknown = EXCLUDE
    
    community_id = ma.UUID(required=True)

    @post_load
    def convert_uuid_to_hex(self, data, **kwargs):
        """Convert all UUID fields to their 32-character hexadecimal equivalent."""
        for key in data:
            value = data[key]
            if isinstance(value, uuid.UUID):
                data[key] = data[key].hex
        return data


class CommunityUrlParamsSchema(UrlParamsSchema):
    """Class to Deserialize information from url parameters
    for community resources.
    """

    topic = EnumField(CommunityTopic)
    city = ma.Str(validate=validate.Length(min=1, max=64))
    state = ma.Str(validate=validate.Length(min=1, max=32))
    country = ma.Str(validate=validate.Length(min=1, max=32))

    @validates_schema
    def validate_location(self, data, **kwargs):
        """Raise a ValidationError if the url parameters for a location are invalid."""
        if "city" in data:
            if "state" not in data or "country" not in data:
                raise ValidationError(
                    "Insufficient location details were provided and the given location"
                    + " could not be determined"
                )
        if "state" in data and "country" not in data:
            raise ValidationError(
                    "Insufficient location details were provided and the given location"
                    + " could not be determined"
                )
        return data

