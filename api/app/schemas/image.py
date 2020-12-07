"""This module contains the marshmallow schema used for
serializing and deserializing Image models.
"""


from app.extensions import ma
from app.models import ImageType
from marshmallow import validate


class ImageSchema(ma.Schema):
    """Class to serialize and deserialize image models."""

    id = ma.UUID(required=True)
    image_type = ma.Str(required=True, validate=validate.OneOf(
        [image_type.name for image_type in ImageType]
    ))
    url = ma.Url(required=True)
    height = ma.Integer(required=True)
    width = ma.Integer(required=True)
    uploaded_at = ma.DateTime(required=True) # defaults to iso 8601
    