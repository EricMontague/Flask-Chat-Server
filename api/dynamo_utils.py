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
        KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"},],
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
            {"AttributeName": "PartitionKey", "KeyType": "HASH"},
            {"AttributeName": "SortKey", "KeyType": "RANGE"},
        ],
        AttributeDefinitions=[
            {"AttributeName": "PartitionKey", "AttributeType": "S"},
            {"AttributeName": "SortKey", "AttributeType": "S"},
        ],
        GlobalSecondaryIndexes=[
            {
                "IndexName": "CommunityMembersIndex",
                "KeySchema": [
                    {"AttributeName": "PartitionKey", "KeyType": "HASH"},
                    {"AttributeName": "SortKey", "KeyType": "RANGE"},
                ],
                "Projection": {"ProjectionType": "ALL"},
                "ProvisionedThroughput": {
                    "ReadCapacityUnits": os.environ.get("AWS_DYNAMODB_INDEX_RCU", 5),
                    "WriteCapacityUnits": os.environ.get("AWS_DYNAMODB_INDEX_WCU", 5),
                },
            },
            {
                "IndexName": "CommunityGroupChatsIndex",
                "KeySchema": [
                    {"AttributeName": "PartitionKey", "KeyType": "HASH"},
                    {"AttributeName": "SortKey", "KeyType": "RANGE"},
                ],
                "Projection": {"ProjectionType": "ALL"},
                "ProvisionedThroughput": {
                    "ReadCapacityUnits": os.environ.get("AWS_DYNAMODB_INDEX_RCU", 5),
                    "WriteCapacityUnits": os.environ.get("AWS_DYNAMODB_INDEX_WCU", 5),
                },
            },
            {
                "IndexName": "CommunitiesByLocationIndex",
                "KeySchema": [
                    {"AttributeName": "PartitionKey", "KeyType": "HASH"},
                    {"AttributeName": "SortKey", "KeyType": "RANGE"},
                ],
                "Projection": {"ProjectionType": "ALL"},
                "ProvisionedThroughput": {
                    "ReadCapacityUnits": os.environ.get("AWS_DYNAMODB_INDEX_RCU", 5),
                    "WriteCapacityUnits": os.environ.get("AWS_DYNAMODB_INDEX_WCU", 5),
                },
            },
            {
                "IndexName": "CommunitiesByTopicIndex",
                "KeySchema": [
                    {"AttributeName": "PartitionKey", "KeyType": "HASH"},
                    {"AttributeName": "SortKey", "KeyType": "RANGE"},
                ],
                "Projection": {"ProjectionType": "ALL"},
                "ProvisionedThroughput": {
                    "ReadCapacityUnits": os.environ.get("AWS_DYNAMODB_INDEX_RCU", 5),
                    "WriteCapacityUnits": os.environ.get("AWS_DYNAMODB_INDEX_WCU", 5),
                },
            },
        ],
        ProvisionedThroughput={
            "ReadCapacityUnits": os.environ.get("AWS_DYNAMODB_TABLE_RCU", 5),
            "WriteCapacityUnits": os.environ.get("AWS_DYNAMODB_TABLE_WCU", 5),
        },
    )
    return table


def create_group_chats_table():
    """Create the Group Chats table in DynamoDB."""
    table = dynamodb.create_table(
        TableName="GroupChats",
        KeySchema=[
            {"AttributeName": "PartitionKey", "KeyType": "HASH"},
            {"AttributeName": "SortKey", "KeyType": "RANGE"},
        ],
        AttributeDefinitions=[
            {"AttributeName": "PartitionKey", "AttributeType": "S"},
            {"AttributeName": "SortKey", "AttributeType": "S"},
        ],
        GlobalSecondaryIndexes=[
            {
                "IndexName": "UserGroupChatsIndex",
                "KeySchema": [
                    {"AttributeName": "PartitionKey", "KeyType": "HASH"},
                    {"AttributeName": "SortKey", "KeyType": "RANGE"},
                ],
                "Projection": {"ProjectionType": "ALL"},
                "ProvisionedThroughput": {
                    "ReadCapacityUnits": os.environ.get("AWS_DYNAMODB_INDEX_RCU", 5),
                    "WriteCapacityUnits": os.environ.get("AWS_DYNAMODB_INDEX_WCU", 5),
                },
            }
        ],
        ProvisionedThroughput={
            "ReadCapacityUnits": os.environ.get("AWS_DYNAMODB_TABLE_RCU", 5),
            "WriteCapacityUnits": os.environ.get("AWS_DYNAMODB_TABLE_WCU", 5),
        },
    )
    return table


def create_private_chats_table():
    """Create the Private Chats table in DynamoDB."""
    table = dynamodb.create_table(
        TableName="PrivateChats",
        KeySchema=[
            {"AttributeName": "PartitionKey", "KeyType": "HASH"},
            {"AttributeName": "SortKey", "KeyType": "RANGE"},
        ],
        AttributeDefinitions=[
            {"AttributeName": "PartitionKey", "AttributeType": "S"},
            {"AttributeName": "SortKey", "AttributeType": "S"},
        ],
        GlobalSecondaryIndexes=[
            {
                "IndexName": "UserPrivateChatsIndex",
                "KeySchema": [
                    {"AttributeName": "PartitionKey", "KeyType": "HASH"},
                    {"AttributeName": "SortKey", "KeyType": "RANGE"},
                ],
                "Projection": {"ProjectionType": "ALL"},
                "ProvisionedThroughput": {
                    "ReadCapacityUnits": os.environ.get("AWS_DYNAMODB_INDEX_RCU", 5),
                    "WriteCapacityUnits": os.environ.get("AWS_DYNAMODB_INDEX_WCU", 5),
                },
            }
        ],
        ProvisionedThroughput={
            "ReadCapacityUnits": os.environ.get("AWS_DYNAMODB_TABLE_RCU", 5),
            "WriteCapacityUnits": os.environ.get("AWS_DYNAMODB_TABLE_WCU", 5),
        },
    )
    return table


def create_notifications_table():
    """Create the Notifications table in DynamoDB."""
    table = dynamodb.create_table(
        TableName="Notifications",
        KeySchema=[
            {"AttributeName": "PartitionKey", "KeyType": "HASH"},
            {"AttributeName": "SortKey", "KeyType": "RANGE"},
        ],
        AttributeDefinitions=[
            {"AttributeName": "PartitionKey", "AttributeType": "S"},
            {"AttributeName": "SortKey", "AttributeType": "S"},
        ],
        ProvisionedThroughput={
            "ReadCapacityUnits": os.environ.get("AWS_DYNAMODB_TABLE_RCU", 5),
            "WriteCapacityUnits": os.environ.get("AWS_DYNAMODB_TABLE_WCU", 5),
        },
    )
    return table


def create_chat_requests_table():
    """Create the ChatRequests table in DynamoDB."""
    table = dynamodb.create_table(
        TableName="ChatRequests",
        KeySchema=[
            {"AttributeName": "PartitionKey", "KeyType": "HASH"},
            {"AttributeName": "SortKey", "KeyType": "RANGE"},
        ],
        AttributeDefinitions=[
            {"AttributeName": "PartitionKey", "AttributeType": "S"},
            {"AttributeName": "SortKey", "AttributeType": "S"},
            {"AttributeName": "PendingId", "AttributeType": "S"},
        ],
        GlobalSecondaryIndexes=[
            {
                "IndexName": "PendingChatRequestsIndex",
                "KeySchema": [
                    {"AttributeName": "PartitionKey", "KeyType": "HASH"},
                    {"AttributeName": "PendingId", "KeyType": "RANGE"},
                ],
                "Projection": {"ProjectionType": "ALL"},
                "ProvisionedThroughput": {
                    "ReadCapacityUnits": os.environ.get("AWS_DYNAMODB_INDEX_RCU", 5),
                    "WriteCapacityUnits": os.environ.get("AWS_DYNAMODB_INDEX_WCU", 5),
                },
            }
        ],
        ProvisionedThroughput={
            "ReadCapacityUnits": os.environ.get("AWS_DYNAMODB_TABLE_RCU", 5),
            "WriteCapacityUnits": os.environ.get("AWS_DYNAMODB_TABLE_WCU", 5),
        },
    )
    return table


def delete_table(table_name):
    """Delete a table from DynamoDB"""
    table = dynamodb.Table(table_name)
    response = table.delete()
    return response

