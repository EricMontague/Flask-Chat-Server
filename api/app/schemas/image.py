"""This module contains the marshmallow schema used for
serializing and deserializing Image models.
"""


from app.extensions import ma
from marshmallow import validate


class ImageSchema(ma.Schema):
    """Class to serialize and deserialize image models."""

    url = ma.Url(required=True)
    height = ma.Integer(required=True, validate=validate.Range(min=1, max=2000))
    width = ma.Integer(required=True, validate=validate.Range(min=1, max=2000))
    