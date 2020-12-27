"""This module contains all of the mapper classes for the application
models.
"""


from app.dynamodb.mapper import ModelMapper
from app.dynamodb.constants import PrimaryKeyPrefix, ItemType
from app.models import (
    User,
    Username,
    UserEmail,
    Role,
    RoleName,
    RolePermission,
    Location,
    Image,
    ImageType,
    Community,
    CommunityMembership,
    CommunityName,
    CommunityTopic,
)


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


class CommunityMapper(ModelMapper):
    """Class to serialize and deserialize Community models to and from
    DynamoDB items.
    """

    class Meta:
        model = Community
        fields = (
            "_id",
            "name",
            "description",
            "topic",
            "avatar",
            "cover_photo",
            "location",
            "_created_at",
        )
        partition_key_attribute = "_id"
        sort_key_attribute = "_id"
        type_ = ItemType.COMMUNITY.name

    ENUMS = {"topic": CommunityTopic}
    NESTED_MAPPERS = {
        "avatar": ImageMapper(ignore_partition_key=True),
        "cover_photo": ImageMapper(ignore_partition_key=True),
        "location": LocationMapper(ignore_partition_key=True),
    }


class CommunityNameMapper(ModelMapper):
    """Class to serialize and deserialize CommunityName models to and from
    DynamoDB items.
    """

    class Meta:
        model = CommunityName
        fields = ("community_id", "name")
        partition_key_attribute = "name"
        sort_key_attribute = "name"
        type_ = ItemType.COMMUNITY_NAME.name


class CommunityMembershipMapper(ModelMapper):
    """Class to serialize and deserialize CommunityMembership models to and from
    DynamoDB items.
    """

    class Meta:
        model = CommunityMembership
        fields = ("community_id", "user_id", "created_at", "is_founder")
        partition_key_attribute = "community_id"
        partition_key_prefix = PrimaryKeyPrefix.COMMUNITY
        sort_key_prefix = PrimaryKeyPrefix.USER
        sort_key_attribute = "user_id"
        type_ = ItemType.COMMUNITY_MEMBERSHIP.name

