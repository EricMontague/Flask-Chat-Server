"""This module contains classes for serializing and deserializing
models that are commonly used with other models to and from DynamoDB
items.
"""


from app.dynamodb_mappers.mapper_core import ModelMapper
from app.models import Location, Image, ImageType


class LocationMapper(ModelMapper):
    """Class to serialize and deserialize location models to and from
    DynamoDB items.
    """

    class Meta:
        model = Location
        fields = ("city", "state", "country")


class ImageMapper(ModelMapper):
    """Class to serialize and deserialize image models to and from
    DynamoDB items.
    """

    class Meta:
        model = Image
        fields = ("id", "image_type", "url", "height", "width", "uploaded_at")

    ENUMS = {"image_type": ImageType}

