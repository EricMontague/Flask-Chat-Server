"""This module contains enums and constants useful for working with DynamoDB."""


from enum import Enum


class ItemType(Enum):
    """Class to represent an item type in DynamoDB."""

    USER = 0
    COMMUNITY = 1
    COMMUNITY_MEMBERSHIP = 2
    USER_EMAIL = 3
    USERNAME = 4


class PrimaryKeyPrefix:
    """Class to represent a key prefix in DynamoDB."""

    USER = "USER#"
    USER_EMAIL = "USEREMAIL#"
    USERNAME = "USERNAME#"
    NOTIFICATION = "NOTIFICATION#"
    COMMUNITY = "COMMUNITY#"
    GROUP_CHAT = "GROUPCHAT#"
    PRIVATE_CHAT = "PRIVATECHAT#"
    TOPIC = "TOPIC#"
    COUNTRY = "COUNTRY#"
    STATE = "STATE#"
    CITY = "CITY#"
    MESSAGE = "MESSAGE#"
    CHAT_REQUEST = "CHATREQUEST#"
    PENDING_CHAT_REQUEST = "PENDING#"
