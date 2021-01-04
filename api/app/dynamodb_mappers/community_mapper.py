"""This module contains classes for serializing and deserializing
Community models and other related models to and from DynamoDB
items.
"""


from app.dynamodb_mappers.mapper_core import ModelMapper
from app.dynamodb_mappers.constants import ItemType, PrimaryKeyPrefix
from app.dynamodb_mappers.common_mappers import ImageMapper, LocationMapper
from app.models import Community, CommunityMembership, CommunityName, CommunityTopic


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
