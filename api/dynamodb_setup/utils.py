"""This file contains functions for performing common setup operations
for Dynamo tables.
"""


import os
import boto3
from dynamodb_setup.global_secondary_indexes import (
    COMMUNITIES_GSI,
    CHAT_REQUESTS_GSI,
    PRIVATE_CHATS_GSI,
    GROUP_CHATS_GSI
)


dynamodb = boto3.resource("dynamodb")



def create_users_table():
    """Create the Users table in DynamoDB."""
    table = dynamodb.create_table(
        TableName="Users",
        KeySchema=[
            {"AttributeName": "PartitionKey", "KeyType": "HASH"},
            {"AttributeName": "SortKey", "KeyType": "RANGE"}
        ],
        AttributeDefinitions=[
            {"AttributeName": "PartitionKey", "AttributeType": "S"},
            {"AttributeName": "SortKey", "AttributeType": "S"}
        ],
        GlobalSecondaryIndexes=[
            COMMUNITIES_GSI,
            CHAT_REQUESTS_GSI,
            PRIVATE_CHATS_GSI,
            GROUP_CHATS_GSI
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

