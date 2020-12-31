"""This module contains enums and constants useful for working with DynamoDB."""


from enum import Enum


class ItemType(Enum):
    """Class to represent an item type in DynamoDB."""

    USER = 1
    COMMUNITY = 2
    COMMUNITY_MEMBERSHIP = 3
    USER_EMAIL = 4
    USERNAME = 5
    COMMUNITY_NAME = 6
    NOTIFICATION = 7
    PRIVATE_CHAT = 8
    PRIVATE_CHAT_MEMBER = 9
    PRIVATE_CHAT_MESSAGE = 10


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
    PRIVATE_CHAT_MESSAGE = "PRIVATE_CHAT_MESSAGE#"
