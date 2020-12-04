"""This module contains the definitions for the GSI's in DynamoDB."""


import os


COMMUNITIES_GSI = {
    "IndexName": "CommunitiesIndex",
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

GROUP_CHATS_GSI = {
    "IndexName": "GroupChatsIndex",
    "KeySchema": [
        {"AttributeName": "PartitionKey", "KeyType": "HASH"},
        {"AttributeName": "SortKey", "KeyType": "RANGE"},
    ],
    "Projection": {"ProjectionType": "ALL"},
    "ProvisionedThroughput": {
        "ReadCapacityUnits": os.environ.get("AWS_DYNAMODB_INDEX_RCU", 5),
        "WriteCapacityUnits": os.environ.get("AWS_DYNAMODB_INDEX_WCU", 5),
    }
}


PRIVATE_CHATS_GSI = {
    "IndexName": "PrivateChatsIndex",
    "KeySchema": [
        {"AttributeName": "PartitionKey", "KeyType": "HASH"},
        {"AttributeName": "SortKey", "KeyType": "RANGE"},
    ],
    "Projection": {"ProjectionType": "ALL"},
    "ProvisionedThroughput": {
        "ReadCapacityUnits": os.environ.get("AWS_DYNAMODB_INDEX_RCU", 5),
        "WriteCapacityUnits": os.environ.get("AWS_DYNAMODB_INDEX_WCU", 5),
    }
}


CHAT_REQUESTS_GSI = {
    "IndexName": "ChatRequestsIndex",
    "KeySchema": [
        {"AttributeName": "PartitionKey", "KeyType": "HASH"},
        {"AttributeName": "SortKey", "KeyType": "RANGE"},
    ],
    "Projection": {"ProjectionType": "ALL"},
    "ProvisionedThroughput": {
        "ReadCapacityUnits": os.environ.get("AWS_DYNAMODB_INDEX_RCU", 5),
        "WriteCapacityUnits": os.environ.get("AWS_DYNAMODB_INDEX_WCU", 5),
    }
}
