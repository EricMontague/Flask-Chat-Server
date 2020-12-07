"""This module contains the marshmallow schema for serializing
and deserializing Location models.
"""


from app.extensions import ma


class LocationSchema(ma.Schema):
    """Class to serialize and deserialize Location models."""

    city = ma.Str(required=True)
    state = ma.Str(required=True)
    country = ma.Str(required=True)