"""This file contains functions for performing common setup operations
for Dynamo tables.
"""


import os
import boto3
from dynamodb_setup.global_secondary_indexes import (
    INVERTED_GSI,
    COMMUNITIES_BY_LOCATION_GSI,
    COMMUNITIES_BY_TOPIC_GSI,
)


dynamodb = boto3.resource("dynamodb")


def create_users_table():
    """Create the Users table in DynamoDB."""
    table = dynamodb.create_table(
        TableName="Users",
        KeySchema=[
            {"AttributeName": "PK", "KeyType": "HASH"},
            {"AttributeName": "SK", "KeyType": "RANGE"},
        ],
        AttributeDefinitions=[
            {"AttributeName": "PK", "AttributeType": "S"},
            {"AttributeName": "SK", "AttributeType": "S"},
            {"AttributeName": "country", "AttributeType": "S"},
            {"AttributeName": "state_city", "AttributeType": "S"},
            {"AttributeName": "topic", "AttributeType": "S"},
            {"AttributeName": "community_id", "AttributeType": "S"},
            {"AttributeName": "request_status_datetime", "AttributeType": "S"},
            {"AttributeName": "group_chat_id", "AttributeType": "S"},
        ],
        GlobalSecondaryIndexes=[
            INVERTED_GSI,
            COMMUNITIES_BY_LOCATION_GSI,
            COMMUNITIES_BY_TOPIC_GSI,
        ],
        ProvisionedThroughput={
            "ReadCapacityUnits": os.environ.get("AWS_DYNAMODB_RCU", 5),
            "WriteCapacityUnits": os.environ.get("AWS_DYNAMODB_WCU", 5),
        },
    )
    return table


def delete_users_table():
    """Delete the Users table from DynamoDB"""
    table = dynamodb.Table("Users")
    response = table.delete()
    return response

