"""This module contains the definitions for the GSI's in DynamoDB."""


import os


INVERTED_GSI = {
    "IndexName": "InvertedIndex",
    "KeySchema": [
        {"AttributeName": "SK", "KeyType": "HASH"},
        {"AttributeName": "PK", "KeyType": "RANGE"},
    ],
    "Projection": {"ProjectionType": "ALL"},
    "ProvisionedThroughput": {
        "ReadCapacityUnits": os.environ.get("AWS_DYNAMODB_INDEX_RCU", 5),
        "WriteCapacityUnits": os.environ.get("AWS_DYNAMODB_INDEX_WCU", 5),
    },
}

COMMUNITIES_BY_LOCATION_GSI = {
    "IndexName": "CommunitiesByLocation",
    "KeySchema": [
        {"AttributeName": "country", "KeyType": "HASH"},
        {"AttributeName": "state_city", "KeyType": "RANGE"},
    ],
    "Projection": {"ProjectionType": "ALL"},
    "ProvisionedThroughput": {
        "ReadCapacityUnits": os.environ.get("AWS_DYNAMODB_INDEX_RCU", 5),
        "WriteCapacityUnits": os.environ.get("AWS_DYNAMODB_INDEX_WCU", 5),
    },
}


COMMUNITIES_BY_TOPIC_GSI = {
    "IndexName": "CommunitiesByTopic",
    "KeySchema": [
        {"AttributeName": "topic", "KeyType": "HASH"},
        {"AttributeName": "community_id", "KeyType": "RANGE"},
    ],
    "Projection": {"ProjectionType": "ALL"},
    "ProvisionedThroughput": {
        "ReadCapacityUnits": os.environ.get("AWS_DYNAMODB_INDEX_RCU", 5),
        "WriteCapacityUnits": os.environ.get("AWS_DYNAMODB_INDEX_WCU", 5),
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
#         "ReadCapacityUnits": os.environ.get("AWS_DYNAMODB_INDEX_RCU", 5),
#         "WriteCapacityUnits": os.environ.get("AWS_DYNAMODB_INDEX_WCU", 5),
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
#         "ReadCapacityUnits": os.environ.get("AWS_DYNAMODB_INDEX_RCU", 5),
#         "WriteCapacityUnits": os.environ.get("AWS_DYNAMODB_INDEX_WCU", 5),
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
        "ReadCapacityUnits": os.environ.get("AWS_DYNAMODB_INDEX_RCU", 5),
        "WriteCapacityUnits": os.environ.get("AWS_DYNAMODB_INDEX_WCU", 5),
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
        "ReadCapacityUnits": os.environ.get("AWS_DYNAMODB_INDEX_RCU", 5),
        "WriteCapacityUnits": os.environ.get("AWS_DYNAMODB_INDEX_WCU", 5),
    },
}
