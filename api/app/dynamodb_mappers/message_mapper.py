"""This module contains classes for serializing and deserializing
Message models and other related models to and from DynamoDB
items.
"""


from app.dynamodb_mappers.mapper_core import ModelMapper
from app.dynamodb_mappers.constants import ItemType, PrimaryKeyPrefix
from app.models import Message, Reaction


class MessageMapper(ModelMapper):
    """Class to serialize and deserialize Message models 
    to and from DynamoDB items.
    """

    class Meta:
        model = Message
        fields = (
            "_id",
            "_chat_id",
            "_user_id",
            "_content",
            "_created_at",
            "_reactions",
            "_editted",
        )
        partition_key_attribute = "_chat_id"
        sort_key_attribute = "_id"
        attributes_to_monkey_patch = ("_reactions",)

    ENUMS = {"_reactions": Reaction}


class PrivateChatMessageMapper(MessageMapper):
    """Class to serialize and deserialize Message models 
    to and from DynamoDB items for private chats.
    """

    class Meta(MessageMapper.Meta):
        partition_key_prefix = PrimaryKeyPrefix.PRIVATE_CHAT
        sort_key_prefix = PrimaryKeyPrefix.PRIVATE_CHAT_MESSAGE
        type_ = ItemType.PRIVATE_CHAT_MESSAGE.name


class GroupChatMessageMapper(MessageMapper):
    """Class to serialize and deserialize Message models 
    to and from DynamoDB items for group chats.
    """

    class Meta(MessageMapper.Meta):
        partition_key_prefix = PrimaryKeyPrefix.GROUP_CHAT
        sort_key_prefix = PrimaryKeyPrefix.GROUP_CHAT_MESSAGE
        type_ = ItemType.GROUP_CHAT_MESSAGE.name
