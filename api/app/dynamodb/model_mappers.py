"""This module contains all of the mapper classes for the application
models.
"""


from app.dynamodb.mapper import ModelMapper
from app.models import User, Role, RoleName, RolePermission, Location, Image, ImageType


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


class RoleMapper(ModelMapper):
    """Class to serialize and deserialize role models to and from
    DynamoDB items.
    """

    class Meta:
        model = Role
        fields = ("name", "permissions")


class UserMapper(ModelMapper):
    """Class to serialize and deserialize user models to and from
    DynamoDB items.
    """

    class Meta:
        model = User
        fields = (
            "_id",
            "name",
            "username",
            "_password_hash",
            "email",
            "_created_at",
            "last_seen_at",
            "role",
            "bio",
            "location",
            "avatar",
            "cover_photo",
            "is_online",
        )
        partition_key_attribute = "_id"
        sort_key_attribute = "_id"

    NESTED_MAPPERS = {
        "location": LocationMapper,
        "avatar": ImageMapper,
        "cover_photo": ImageMapper,
        "role": RoleMapper,
    }

