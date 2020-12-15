"""This module contains the schema for serializing and deserializing
information from url parameters
"""


from app.extensions import ma
from marshmallow import EXCLUDE, validates_schema, ValidationError


class UrlParamsSchema(ma.Schema):
    """Class to serialize and deserialize information from url parameters"""

    class Meta:
        unknown = EXCLUDE

    per_page = ma.Integer()
    next_cursor = ma.Str(data_key="next")
    prev_cursor = ma.Str(data_key="prev")

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
