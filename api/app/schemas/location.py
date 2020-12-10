"""This module contains the marshmallow schema for serializing
and deserializing Location models.
"""


from app.extensions import ma
from marshmallow import validate


class LocationSchema(ma.Schema):
    """Class to serialize and deserialize Location models."""

    city = ma.Str(required=True, validate=validate.Length(min=1, max=64))
    state = ma.Str(required=True, validate=validate.Length(min=1, max=32))
    country = ma.Str(required=True, validate=validate.Length(min=1, max=32))