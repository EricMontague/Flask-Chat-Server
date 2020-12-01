"""This file contains functions for performing common setup operations
for Dynamo tables.
"""


import os
import boto3


dynamodb = boto3.resource("dynamodb")


def create_users_table():
    """Create the Users table in DynamoDB."""
    table = dynamodb.create_table(
        TableName="Users",
        KeySchema=[{"AttributeName": "user_id", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "user_id", "AttributeType": "S"},],
        ProvisionedThroughput={
            "ReadCapacityUnits": os.environ.get("AWS_DYNAMODB_RCU", 5),
            "WriteCapacityUnits": os.environ.get("AWS_DYNAMODB_WCU", 5),
        },
    )
    return table


def create_communities_table():
    """Create the Communities table in DynamoDB."""
    table = dynamodb.create_table(
        TableName="Communities",
        KeySchema=[
            {"AttributeName": "PK", "KeyType": "HASH"}, 
            {"AttributeName": "SK", "KeyType": "RANGE"}
        ],
        AttributeDefitions=[
            {"AttributeName": "PK", "AttributeType": "S"},
            {"AttributeName": "SK", "AttributeType": "S"}
        ],
        GlobalSecondaryIndexes=[
            {
                "IndexName": "CommunityMembersIndex",
                "KeySchema": [
                    {"AttributeName": "PK", "KeyType": "HASH"}, 
                    {"AttributeName": "SK", "KeyType": "RANGE"}
                ],
                "Projection": {
                    "ProjectionType": "ALL"
                },
                "ProvisionedThroughPut": {
                    "ReadCapacityUnits": os.environ.get("AWS_DYNAMODB_INDEX_RCU", 5),
                    "WriteCapacityUnits": os.environ.get("AWS_DYNAMODB_INDEX_WCU", 5),
                }
            },
            {
                "IndexName": "CommunityGroupChatsIndex",
                "KeySchema": [
                    {"AttributeName": "PK", "KeyType": "HASH"}, 
                    {"AttributeName": "SK", "KeyType": "RANGE"}
                ],
                "Projection": {
                    "ProjectionType": "ALL"
                },
                "ProvisionedThroughPut": {
                    "ReadCapacityUnits": os.environ.get("AWS_DYNAMODB_INDEX_RCU", 5),
                    "WriteCapacityUnits": os.environ.get("AWS_DYNAMODB_INDEX_WCU", 5),
                }
            },
            {
                "IndexName": "CommunityLocationsIndex",
                "KeySchema": [
                    {"AttributeName": "PK", "KeyType": "HASH"}, 
                    {"AttributeName": "SK", "KeyType": "RANGE"}
                ],
                "Projection": {
                    "ProjectionType": "ALL"
                },
                "ProvisionedThroughPut": {
                    "ReadCapacityUnits": os.environ.get("AWS_DYNAMODB_INDEX_RCU", 5),
                    "WriteCapacityUnits": os.environ.get("AWS_DYNAMODB_INDEX_WCU", 5),
                }
            }
        ],
        ProvisionedThroughput={
            "ReadCapacityUnits": os.environ.get("AWS_DYNAMODB_TABLE_RCU", 5),
            "WriteCapacityUnits": os.environ.get("AWS_DYNAMODB_TABLE_WCU", 5),
        }
    )
    return table


def create_group_chats_table():
    """Create the Group Chats table in DynamoDB."""
    table = dynamodb.create_table(
        TableName="Group Chats",
        KeySchema=[
            {"AttributeName": "PK", "KeyType": "HASH"}, 
            {"AttributeName": "SK", "KeyType": "RANGE"}
        ],
        AttributeDefitions=[
            {"AttributeName": "PK", "AttributeType": "S"},
            {"AttributeName": "SK", "AttributeType": "S"}
        ],
        GlobalSecondaryIndexes=[
            {
                "IndexName": "UserGroupChatsIndex",
                "KeySchema": [
                    {"AttributeName": "PK", "KeyType": "HASH"}, 
                    {"AttributeName": "SK", "KeyType": "RANGE"}
                ],
                "Projection": {
                    "ProjectionType": "ALL"
                },
                "ProvisionedThroughPut": {
                    "ReadCapacityUnits": os.environ.get("AWS_DYNAMODB_INDEX_RCU", 5),
                    "WriteCapacityUnits": os.environ.get("AWS_DYNAMODB_INDEX_WCU", 5),
                }
            }
        ],
        ProvisionedThroughput={
            "ReadCapacityUnits": os.environ.get("AWS_DYNAMODB_TABLE_RCU", 5),
            "WriteCapacityUnits": os.environ.get("AWS_DYNAMODB_TABLE_WCU", 5),
        }
    )
    return table


def create_private_chats_table():
    """Create the Private Chats table in DynamoDB."""
    table = dynamodb.create_table(
        TableName="Private Chats",
        KeySchema=[
            {"AttributeName": "PK", "KeyType": "HASH"}, 
            {"AttributeName": "SK", "KeyType": "RANGE"}
        ],
        AttributeDefitions=[
            {"AttributeName": "PK", "AttributeType": "S"},
            {"AttributeName": "SK", "AttributeType": "S"}
        ],
        GlobalSecondaryIndexes=[
            {
                "IndexName": "UserPrivateChatsIndex",
                "KeySchema": [
                    {"AttributeName": "PK", "KeyType": "HASH"}, 
                    {"AttributeName": "SK", "KeyType": "RANGE"}
                ],
                "Projection": {
                    "ProjectionType": "ALL"
                },
                "ProvisionedThroughPut": {
                    "ReadCapacityUnits": os.environ.get("AWS_DYNAMODB_INDEX_RCU", 5),
                    "WriteCapacityUnits": os.environ.get("AWS_DYNAMODB_INDEX_WCU", 5),
                }
            }
        ],
        ProvisionedThroughput={
            "ReadCapacityUnits": os.environ.get("AWS_DYNAMODB_TABLE_RCU", 5),
            "WriteCapacityUnits": os.environ.get("AWS_DYNAMODB_TABLE_WCU", 5),
        }
    )
    return table


def create_notifications_table():
    """Create the Notifications table in DynamoDB."""
    table = dynamodb.create_table(
        TableName="Notifications",
        KeySchema=[
            {"AttributeName": "PK", "KeyType": "HASH"}, 
            {"AttributeName": "SK", "KeyType": "RANGE"}
        ],
        AttributeDefitions=[
            {"AttributeName": "PK", "AttributeType": "S"},
            {"AttributeName": "SK", "AttributeType": "S"}
        ],
        GlobalSecondaryIndexes=[
            {
                "IndexName": "PendingChatRequestsIndex",
                "KeySchema": [
                    {"AttributeName": "PK", "KeyType": "HASH"}, 
                    {"AttributeName": "SK", "KeyType": "RANGE"}
                ],
                "Projection": {
                    "ProjectionType": "ALL"
                },
                "ProvisionedThroughPut": {
                    "ReadCapacityUnits": os.environ.get("AWS_DYNAMODB_INDEX_RCU", 5),
                    "WriteCapacityUnits": os.environ.get("AWS_DYNAMODB_INDEX_WCU", 5),
                }
            }
        ],
        ProvisionedThroughput={
            "ReadCapacityUnits": os.environ.get("AWS_DYNAMODB_TABLE_RCU", 5),
            "WriteCapacityUnits": os.environ.get("AWS_DYNAMODB_TABLE_WCU", 5),
        }
    )
    return table



def create_chat_requests_table():
    """Create the ChatRequests table in DynamoDB."""
    table = dynamodb.create_table(
        TableName="ChatRequests",
        KeySchema=[
            {"AttributeName": "PK", "KeyType": "HASH"}, 
            {"AttributeName": "SK", "KeyType": "RANGE"}
        ],
        AttributeDefitions=[
            {"AttributeName": "PK", "AttributeType": "S"},
            {"AttributeName": "SK", "AttributeType": "S"}
        ],
        ProvisionedThroughput={
            "ReadCapacityUnits": os.environ.get("AWS_DYNAMODB_TABLE_RCU", 5),
            "WriteCapacityUnits": os.environ.get("AWS_DYNAMODB_TABLE_WCU", 5),
        }
    )
    return table


def delete_table(table_name):
    """Delete a table from DynamoDB"""
    table = dynamodb.Table(table_name)
    response = table.delete()
    return response

