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
        "ReadCapacityUnits": os.environ.get("AWS_DYNAMODB_INDEX_RCU", 25),
        "WriteCapacityUnits": os.environ.get("AWS_DYNAMODB_INDEX_WCU", 25),
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
        "ReadCapacityUnits": os.environ.get("AWS_DYNAMODB_INDEX_RCU", 25),
        "WriteCapacityUnits": os.environ.get("AWS_DYNAMODB_INDEX_WCU", 25),
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
        "ReadCapacityUnits": os.environ.get("AWS_DYNAMODB_INDEX_RCU", 25),
        "WriteCapacityUnits": os.environ.get("AWS_DYNAMODB_INDEX_WCU", 25),
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
        "ReadCapacityUnits": os.environ.get("AWS_DYNAMODB_INDEX_RCU", 25),
        "WriteCapacityUnits": os.environ.get("AWS_DYNAMODB_INDEX_WCU", 25),
    },
}

# GROUP_CHATS_GSI = {
#     "IndexName": "GroupChatsIndex",
#     "KeySchema": [
#         {"AttributeName": "PK", "KeyType": "HASH"},
#         {"AttributeName": "SK", "KeyType": "RANGE"},
#     ],
#     "Projection": {"ProjectionType": "ALL"},
#     "ProvisionedThroughput": {
#         "ReadCapacityUnits": os.environ.get("AWS_DYNAMODB_INDEX_RCU", 25),
#         "WriteCapacityUnits": os.environ.get("AWS_DYNAMODB_INDEX_WCU", 25),
#     }
# }


# PRIVATE_CHATS_GSI = {
#     "IndexName": "PrivateChatsIndex",
#     "KeySchema": [
#         {"AttributeName": "PK", "KeyType": "HASH"},
#         {"AttributeName": "SK", "KeyType": "RANGE"},
#     ],
#     "Projection": {"ProjectionType": "ALL"},
#     "ProvisionedThroughput": {
#         "ReadCapacityUnits": os.environ.get("AWS_DYNAMODB_INDEX_RCU", 25),
#         "WriteCapacityUnits": os.environ.get("AWS_DYNAMODB_INDEX_WCU", 25),
#     }
# }


USER_PENDING_REQUESTS_GSI = {
    "IndexName": "UserPendingRequestsIndex",
    "KeySchema": [
        {"AttributeName": "PK", "KeyType": "HASH"},
        {"AttributeName": "request_status_datetime", "KeyType": "RANGE"},
    ],
    "Projection": {"ProjectionType": "ALL"},
    "ProvisionedThroughput": {
        "ReadCapacityUnits": os.environ.get("AWS_DYNAMODB_INDEX_RCU", 25),
        "WriteCapacityUnits": os.environ.get("AWS_DYNAMODB_INDEX_WCU", 25),
    },
}


GROUP_CHAT_PENDING_REQUESTS_GSI = {
    "IndexName": "GroupChatPendingRequestsIndex",
    "KeySchema": [
        {"AttributeName": "group_chat_id", "KeyType": "HASH"},
        {"AttributeName": "request_status_datetime", "KeyType": "RANGE"},
    ],
    "Projection": {"ProjectionType": "ALL"},
    "ProvisionedThroughput": {
        "ReadCapacityUnits": os.environ.get("AWS_DYNAMODB_INDEX_RCU", 25),
        "WriteCapacityUnits": os.environ.get("AWS_DYNAMODB_INDEX_WCU", 25),
    },
}


GSI_LIST = [
    USERS_GSI,
    COMMUNITIES_BY_LOCATION_GSI,
    COMMUNITIES_BY_TOPIC_GSI,
    USER_PENDING_REQUESTS_GSI,
    GROUP_CHAT_PENDING_REQUESTS_GSI,
    INVERTED_GSI
]