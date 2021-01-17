"""This module contains classes for serializing and deserializing
various chat models and other related models to and from DynamoDB
items.
"""


from app.dynamodb_mappers.mapper_core import ModelMapper
from app.dynamodb_mappers.constants import PrimaryKeyPrefix, ItemType
from app.models import PrivateChatMembership, GroupChatMembership, GroupChat, PrivateChat


class PrivateChatMapper(ModelMapper):
    """Class to be used only to serialize PrivateChat models
    to DynamoDB items.
    """

    class Meta:
        model = PrivateChat
        fields = ("_id", "primary_user_id", "secondary_user_id")
        partition_key_attribute = "_id"
        partition_key_prefix = PrimaryKeyPrefix.PRIVATE_CHAT
        sort_key_attribute = "_id"
        sory_key_prefix = PrimaryKeyPrefix.PRIVATE_CHAT
        type_ = ItemType.PRIVATE_CHAT.name


class PrivateChatMembershipMapper(ModelMapper):
    """Class to serialize and deserialize PrivateChatMembership models 
    to and from DynamoDB items.
    """

    class Meta:
        model = PrivateChatMembership
        fields = ("private_chat_id", "user_id", "other_user_id", "created_at")
        partition_key_attribute = "user_id"
        partition_key_prefix = PrimaryKeyPrefix.USER
        sort_key_attribute = "private_chat_id"
        sort_key_prefix = PrimaryKeyPrefix.PRIVATE_CHAT
        type_ = ItemType.PRIVATE_CHAT_MEMBERSHIP.name


class GroupChatMembershipMapper(ModelMapper):
    """Class to serialize and deserialize GroupChatMembership models 
    to and from DynamoDB items.
    """

    class Meta:
        model = GroupChatMembership
        fields = ("group_chat_id", "community_id", "user_id", "created_at")
        partition_key_attribute = "group_chat_id"
        partition_key_prefix = PrimaryKeyPrefix.GROUP_CHAT
        sort_key_attribute = "user_id"
        sort_key_prefix = PrimaryKeyPrefix.USER
        type_ = ItemType.GROUP_CHAT_MEMBERSHIP.name


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
