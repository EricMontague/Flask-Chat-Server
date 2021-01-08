"""This module contains classes for serializing and deserializing
Token models and other related models to and from DynamoDB
items.
"""


from app.dynamodb_mappers.mapper_core import ModelMapper
from app.dynamodb_mappers.constants import ItemType, PrimaryKeyPrefix
from app.models import Token, TokenType


class TokenMapper(ModelMapper):
    """Class to serialize and deserialize token models to and from
    DynamoDB items.
    """

    class Meta:
        model = Token
        fields = (
            "user_id",
            "raw_jwt",
            "expires_on_date",
            "issued_at",
            "token_type",
            "is_blacklisted",
        )
        partition_key_attribute = "user_id"
        partition_key_prefix = PrimaryKeyPrefix.USER
        sort_key_attribute = "raw_jwt"
        sort_key_prefix = PrimaryKeyPrefix.ACCESS_TOKEN
        type_ = ItemType.JWT

    ENUMS = {"token_type": TokenType}

