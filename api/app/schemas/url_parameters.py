"""This module contains the schema for serializing and deserializing
information from url parameters
"""


from app.extensions import ma
from app.schemas.enum_field import EnumField
from app.schemas.location import LocationSchema
from app.models import CommunityTopic
from marshmallow import EXCLUDE, validates_schema, ValidationError, validate


class UrlParamsSchema(ma.Schema):
    """Class to serialize and deserialize information from url parameters"""

    class Meta:
        unknown = EXCLUDE

    per_page = ma.Integer()
    next_cursor = ma.Str(data_key="next")
    # prev_cursor = ma.Str(data_key="prev")

    @validates_schema
    def validate_cursors(self, data, **kwargs):
        """Raise a ValidationError if both the next and previous cursors
        were sent.
        """
        if "next_cursor" in data and "prev_cursor" in data:
            raise ValidationError(
                "Next and previous cursors cannot be present at the same time"
            )
        return data


class CommunityUrlParamsSchema(UrlParamsSchema):
    """Class to serialize and deserialize information from url parameters
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

