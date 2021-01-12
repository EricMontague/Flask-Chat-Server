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
    GROUP_CHAT_MEMBER = 11
    GROUP_CHAT_MESSAGE = 12
    GROUP_CHAT = 13
    COMMUNITY_GROUP_CHAT = 14
    JWT_ACCESS_TOKEN = 15
    JWT_REFRESH_TOKEN = 16


class PrimaryKeyPrefix:
    """Class to represent a key prefix in DynamoDB."""

    USER = "USER#"
    USER_EMAIL = "USEREMAIL#"
    USERNAME = "USERNAME#"
    NOTIFICATION = "NOTIFICATION#"
    COMMUNITY = "COMMUNITY#"
    COMMUNITY_NAME = "COMMUNITYNAME#"
    GROUP_CHAT = "GROUPCHAT#"
    PRIVATE_CHAT = "PRIVATECHAT#"
    TOPIC = "TOPIC#"
    COUNTRY = "COUNTRY#"
    STATE = "STATE#"
    CITY = "CITY#"
    PENDING_CHAT_REQUEST = "PENDING#"
    PRIVATE_CHAT_MESSAGE = "PRIVATE_CHAT_MESSAGE#"
    GROUP_CHAT_MESSAGE = "GROUP_CHAT_MESSAGE#"
    JWT_ACCESS_TOKEN = "JWT_ACCESS_TOKEN#"
    JWT_REFRESH_TOKEN = "JWT_REFRESH_TOKEN#"
