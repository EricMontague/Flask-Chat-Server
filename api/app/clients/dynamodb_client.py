"""This module contains a class that acts as a wrapper around
the boto3 library's DynamoDB resource.
"""

import boto3
from boto3.dynamodb.conditions import Key


class _DynamoDBClient:
    """Class that acts as a wrapper around the boto3 library's
    DynamoDB resource.
    """

    _USERS_TABLE = "Users"

    def __init__(self, endpoint_url=""):
        # Endpoint url used for testing with a local version of DynamoDB
        if endpoint_url:
            self._dynamodb = boto3.resource("dynamodb", endpoint_url=endpoint_url)
        else:
            self._dynamodb = boto3.resource("dynamodb")
        self._users_table = self._dynamodb.Table(self._USERS_TABLE)

    def get_user(self, partition_key):
        response = self._users_table.query(
            Select="ALL_ATTRIBUTES",
            KeyConditionExpression=Key("PartitionKey").eq(partition_key),
            ReturnConsumedCapacity="INDEXES",
            ReturnItemCollectionMetrics="SIZE"
        )
     
        return response

    def put_user(self, user):
        response = self._users_table.put_item(
            Item=user.to_dict(),
            
        )
        return response, response["ResponseMetadata"]["HTTPStatusCode"]

    def update_user(self, partition_key, expression):
        response = self._users_table.update_item(
            Key={"id": partition_key},
            ReturnConsumedCapacity="INDEXES",
            ReturnItemCollectionMetrics="SIZE",
            UpdateExpression=expression.expression,
            ExpressionAttributeNames=expression.attribute_names,
            ExpressionAttributeValues=expression.attribute_values,
        )
        return response, response["ResponseMetadata"]["HTTPStatusCode"]

    def delete_user(self, partition_key):
        response = self._users_table.delete_item(
            Key={"id": partition_key},
            ReturnConsumedCapacity="INDEXES",
            ReturnItemCollectionMetrics="SIZE",
        )
        return response, response["ResponseMetadata"]["HTTPStatusCode"]


dynamodb_client = _DynamoDBClient()
