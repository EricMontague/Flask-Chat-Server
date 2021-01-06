"""This module contains classes for serializing and deserializing
various chat models and other related models to and from DynamoDB
items.
"""


from app.dynamodb_mappers.mapper_core import ModelMapper
from app.dynamodb_mappers.constants import PrimaryKeyPrefix, ItemType
from app.models import PrivateChatMember, GroupChatMember, GroupChat


class PrivateChatMemberMapper(ModelMapper):
    """Class to serialize and deserialize PrivateChatMember models 
    to and from DynamoDB items.
    """

    class Meta:
        model = PrivateChatMember
        fields = ("private_chat_id", "user_id", "other_user_id", "created_at")
        partition_key_attribute = "user_id"
        partition_key_prefix = PrimaryKeyPrefix.USER
        sort_key_attribute = "private_chat_id"
        sort_key_prefix = PrimaryKeyPrefix.PRIVATE_CHAT
        type_ = ItemType.PRIVATE_CHAT_MEMBER.name


class GroupChatMemberMapper(ModelMapper):
    """Class to serialize and deserialize GroupChatMember models 
    to and from DynamoDB items.
    """

    class Meta:
        model = GroupChatMember
        fields = ("group_chat_id", "community_id", "user_id", "created_at")
        partition_key_attribute = "group_chat_id"
        partition_key_prefix = PrimaryKeyPrefix.GROUP_CHAT
        sort_key_attribute = "user_id"
        sort_key_prefix = PrimaryKeyPrefix.USER
        type_ = ItemType.GROUP_CHAT_MEMBER.name


class GroupChatMapper(ModelMapper):
    """Class to serialize and deserialize GroupChat models 
    to and from DynamoDB items.
    """

    class Meta:
        model = GroupChat
        fields = ("_id", "_community_id", "name", "description")
        partition_key_attribute = "_community_id"
        partition_key_prefix = PrimaryKeyPrefix.COMMUNITY
        sort_key_attribute = "_id"
        sort_key_prefix = PrimaryKeyPrefix.GROUP_CHAT
        type_ = ItemType.GROUP_CHAT.name
