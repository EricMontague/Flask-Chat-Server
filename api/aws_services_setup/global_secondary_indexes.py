"""This module contains the definitions for the GSI's in DynamoDB."""


import os


USERS_GSI = {
    "IndexName": "UsersIndex",
    "KeySchema": [
        {"AttributeName": "USERS_GSI_PK", "KeyType": "HASH"},
        {"AttributeName": "USERS_GSI_SK", "KeyType": "RANGE"},
    ],
    "Projection": {"ProjectionType": "ALL"},
    "ProvisionedThroughput": {
        "ReadCapacityUnits": int(os.environ.get("AWS_DYNAMODB_INDEX_RCU", 2)),
        "WriteCapacityUnits": int(os.environ.get("AWS_DYNAMODB_INDEX_WCU", 2)),
    },
}

COMMUNITIES_BY_LOCATION_GSI = {
    "IndexName": "CommunitiesByLocation",
    "KeySchema": [
        {"AttributeName": "COMMUNITIES_BY_LOCATION_GSI_PK", "KeyType": "HASH"},
        {"AttributeName": "COMMUNITIES_BY_LOCATION_GSI_SK", "KeyType": "RANGE"},
    ],
    "Projection": {"ProjectionType": "ALL"},
    "ProvisionedThroughput": {
        "ReadCapacityUnits": int(os.environ.get("AWS_DYNAMODB_INDEX_RCU", 2)),
        "WriteCapacityUnits": int(os.environ.get("AWS_DYNAMODB_INDEX_WCU", 2)),
    },
}


COMMUNITIES_BY_TOPIC_GSI = {
    "IndexName": "CommunitiesByTopic",
    "KeySchema": [
        {"AttributeName": "COMMUNITIES_BY_TOPIC_GSI_PK", "KeyType": "HASH"},
        {"AttributeName": "COMMUNITIES_BY_TOPIC_GSI_SK", "KeyType": "RANGE"},
    ],
    "Projection": {"ProjectionType": "ALL"},
    "ProvisionedThroughput": {
        "ReadCapacityUnits": int(os.environ.get("AWS_DYNAMODB_INDEX_RCU", 2)),
        "WriteCapacityUnits": int(os.environ.get("AWS_DYNAMODB_INDEX_WCU", 2)),
    },
}


INVERTED_GSI = {
    "IndexName": "InvertedIndex",
    "KeySchema": [
        {"AttributeName": "INVERTED_GSI_PK", "KeyType": "HASH"},
        {"AttributeName": "INVERTED_GSI_SK", "KeyType": "RANGE"},
    ],
    "Projection": {"ProjectionType": "ALL"},
    "ProvisionedThroughput": {
        "ReadCapacityUnits": int(os.environ.get("AWS_DYNAMODB_INDEX_RCU", 2)),
        "WriteCapacityUnits": int(os.environ.get("AWS_DYNAMODB_INDEX_WCU", 2)),
    },
}




GSI_LIST = [
    USERS_GSI,
    COMMUNITIES_BY_LOCATION_GSI,
    COMMUNITIES_BY_TOPIC_GSI,
    INVERTED_GSI
]