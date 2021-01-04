"""This module contains classes for serializing and deserializing
User models and other related models to and from DynamoDB
items.
"""


from app.dynamodb_mappers.mapper_core import ModelMapper
from app.dynamodb_mappers.constants import ItemType, PrimaryKeyPrefix
from app.dynamodb_mappers.common_mappers import ImageMapper, LocationMapper
from app.models import User, Username, UserEmail, Role, RoleName, RolePermission


class RoleMapper(ModelMapper):
    """Class to serialize and deserialize role models to and from
    DynamoDB items.
    """

    class Meta:
        model = Role
        fields = ("name", "_permissions")

    ENUMS = {"name": RoleName, "_permissions": RolePermission}


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
        type_ = ItemType.USER.name
        partition_key_attribute = "_id"
        sort_key_attribute = "_id"
        attributes_to_monkey_patch = ("_password_hash",)

    NESTED_MAPPERS = {
        "location": LocationMapper(ignore_partition_key=True),
        "avatar": ImageMapper(ignore_partition_key=True),
        "cover_photo": ImageMapper(ignore_partition_key=True),
        "role": RoleMapper(ignore_partition_key=True),
    }


class UserEmailMapper(ModelMapper):
    """Class to serialize and deserialize UserEmail models to and from
    DynamoDB items.
    """

    class Meta:
        model = UserEmail
        fields = ("user_id", "email")
        partition_key_attribute = "email"
        sort_key_attribute = "email"
        type_ = ItemType.USER_EMAIL.name


class UsernameMapper(ModelMapper):
    """Class to serialize and deserialize Username models to and from
    DynamoDB items.
    """

    class Meta:
        model = Username
        fields = ("user_id", "username")
        partition_key_attribute = "username"
        sort_key_attribute = "username"
        type_ = ItemType.USERNAME.name

