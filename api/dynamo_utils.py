"""This file contains functions for performing common setup operations
for Dynamo tables.
"""


import os
import boto3


dynamodb = boto3.resource("dynamodb")

def create_users_table():
    """Create the users table in DynamoDB."""    
    table = dynamodb.create_table(
        TableName="Users",
        KeySchema=[
            {
                "AttributeName": "userId",
                "KeyType": "HASH"
            }
        ],
        AttributeDefinitions=[
            {
                "AttributeName": "userId",
                "AttributeType": "S"
            },
        ],
        ProvisionedThroughput={
            "ReadCapacityUnits": os.environ.get("AWS_DYNAMODB_RCU", 5),
            "WriteCapacityUnits": os.environ.get("AWS_DYNAMODB_WCU", 5)
        }
    )
    return table


def delete_table(table_name):
    """Delete a table from DynamoDB"""
    table = dynamodb.Table(table_name)
    response = table.delete()
    return response


