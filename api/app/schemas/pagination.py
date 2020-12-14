"""This module contains the schema for serializing and deserializing
pagination information from API requests.
"""


from app.extensions import ma
from marshmallow import EXCLUDE


class PaginationSchema(ma.Schema):
    """Class to serialize and deserialize pagination information."""

    class Meta:
        unknown = EXCLUDE

    per_page = ma.Integer(required=True)
    next_cursor = ma.Str(required=True, data_key="next")
    has_next = ma.Boolean(required=True)
    previous_cursor = ma.Str(required=True, data_key="prev")
    has_prev = ma.Boolean(required=True)
    total = ma.Integer(required=True)
