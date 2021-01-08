"""This file contains functions for performing common setup operations
for AWS services
"""


import os
import boto3
from aws_services_setup.global_secondary_indexes import GSI_LIST


TABLE_NAME = os.environ.get("AWS_DYNAMODB_TABLE_NAME", "ChatAppTable")
BUCKET_NAME = os.environ.get("AWS_S3_BUCKET_NAME", "chat-app-images")
BUCKET_LOCATION = os.environ.get("AWS_S3_BUCKET_LOCATION", "us-east-2")
dynamodb_client = boto3.client(
    "dynamodb", endpoint_url=os.environ.get("AWS_DYNAMODB_ENDPOINT_URL", "http://localhost:8000")
)
s3_client = boto3.client("s3")


def create_dynamodb_table():
    """Create the application's single table in DynamoDB."""
    table = dynamodb_client.create_table(
        TableName=TABLE_NAME,
        KeySchema=[
            {"AttributeName": "PK", "KeyType": "HASH"},
            {"AttributeName": "SK", "KeyType": "RANGE"},
        ],
        AttributeDefinitions=[
            {"AttributeName": "PK", "AttributeType": "S"},
            {"AttributeName": "SK", "AttributeType": "S"},
            {"AttributeName": "USERS_GSI_PK", "AttributeType": "S"},
            {"AttributeName": "USERS_GSI_SK", "AttributeType": "S"},
            {"AttributeName": "COMMUNITIES_BY_TOPIC_GSI_PK", "AttributeType": "S"},
            {"AttributeName": "COMMUNITIES_BY_TOPIC_GSI_SK", "AttributeType": "S"},
            {"AttributeName": "COMMUNITIES_BY_LOCATION_GSI_PK", "AttributeType": "S"},
            {"AttributeName": "COMMUNITIES_BY_LOCATION_GSI_SK", "AttributeType": "S"},
            {"AttributeName": "INVERTED_GSI_PK", "AttributeType": "S"},
            {"AttributeName": "INVERTED_GSI_SK", "AttributeType": "S"},
        ],
        GlobalSecondaryIndexes=GSI_LIST,
        ProvisionedThroughput={
            "ReadCapacityUnits": os.environ.get("AWS_DYNAMODB_RCU", 25),
            "WriteCapacityUnits": os.environ.get("AWS_DYNAMODB_WCU", 25),
        },
    )

    # Setup TTL
    dynamodb_client.update_time_to_live(
        TableName=TABLE_NAME,
        TimeToLiveSpecification={
            "Enabled": True, "AttributeName": "expires_on_date"
        }
    )
    return table


def delete_dynamodb_table():
    """Delete the application's single table from DynamoDB"""
    return dynamodb_client.delete_table(TableName=TABLE_NAME)
    

def create_s3_bucket():
    """Create a bucket in S3."""
    return s3_client.create_bucket(
        Bucket=BUCKET_NAME,
        CreateBucketConfiguration={"LocationConstraint": BUCKET_LOCATION},
    )


def delete_s3_bucket():
    """Delete a bucket from S3."""
    return s3_client.delete_bucket(Bucket=BUCKET_NAME)

