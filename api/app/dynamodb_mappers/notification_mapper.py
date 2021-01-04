"""This module contains classes for serializing and deserializing
Notification models and other related models to and from DynamoDB
items.
"""


from app.dynamodb_mappers.mapper_core import ModelMapper
from app.dynamodb_mappers.constants import ItemType, PrimaryKeyPrefix
from app.models import Notification, NotificationType


class NotificationMapper(ModelMapper):
    """Class to serialize and deserialize Notification models to and
    from DynamoDB items.
    """

    class Meta:
        model = Notification
        fields = (
            "_id",
            "_user_id",
            "_notification_type",
            "_message",
            "_target_url",
            "_created_at",
            "_read",
            "_seen",
        )
        partition_key_attribute = "_user_id"
        partition_key_prefix = PrimaryKeyPrefix.USER
        sort_key_prefix = PrimaryKeyPrefix.NOTIFICATION
        sort_key_attribute = "_id"
        type_ = ItemType.NOTIFICATION.name

    ENUMS = {"_notification_type": NotificationType}
