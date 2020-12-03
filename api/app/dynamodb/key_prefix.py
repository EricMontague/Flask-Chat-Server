"""This module contains a class that holds prefixes for partition
and sort keys in DynamoDB.
"""


class KeyPrefix:
    """Class to represent a key prefix in DynamoDB."""

    USER = "USER#"
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