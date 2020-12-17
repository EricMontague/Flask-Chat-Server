"""This file contains functions for performing common setup operations
for Dynamo tables.
"""


import os
import boto3
from dynamodb_setup.global_secondary_indexes import (
    USERS_GSI,
    COMMUNITIES_BY_LOCATION_GSI,
    COMMUNITIES_BY_TOPIC_GSI,
    USER_PENDING_REQUESTS_GSI,
    GROUP_CHAT_PENDING_REQUESTS_GSI
)


TABLE_NAME = os.environ.get("AWS_DYNAMODB_TABLE_NAME", "ChatAppTable")
dynamodb = boto3.resource("dynamodb")


def create_application_table():
    """Create the application's single table in DynamoDB."""
    table = dynamodb.create_table(
        TableName=TABLE_NAME,
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
            {"AttributeName": "USERS_GSI_SK", "AttributeType": "S"}
        ],
        GlobalSecondaryIndexes=[
            USERS_GSI,
            COMMUNITIES_BY_LOCATION_GSI,
            COMMUNITIES_BY_TOPIC_GSI,
            USER_PENDING_REQUESTS_GSI,
            GROUP_CHAT_PENDING_REQUESTS_GSI
        ],
        ProvisionedThroughput={
            "ReadCapacityUnits": os.environ.get("AWS_DYNAMODB_RCU", 25),
            "WriteCapacityUnits": os.environ.get("AWS_DYNAMODB_WCU", 25),
        },
    )
    return table


def delete_application_table():
    """Delete the application's ginle table from DynamoDB"""
    table = dynamodb.Table(TABLE_NAME)
    response = table.delete()
    return response

