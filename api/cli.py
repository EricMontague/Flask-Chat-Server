"""This file contains various cli commands for automating tasks
such as database table creation, running tests and more.
"""


import click
from aws_services_setup.utils import (
    create_dynamodb_table,
    delete_dynamodb_table,
    create_s3_bucket,
    delete_s3_bucket,
)
from botocore.exceptions import ClientError


@click.group()
def aws():
    pass


@aws.command()
def create_table():
    """Create the single DynamoDB application table"""
    try:
        response = create_dynamodb_table()
        print(f"Successfully created table - {response['TableDescription']['TableName']}")
    except ClientError as err:
        print(err, "\n")


@aws.command()
def delete_table():
    """Delete the single Dynamodb table"""
    try:
        response = delete_dynamodb_table()
        name = response["TableDescription"]["TableName"]
        status = response["TableDescription"]["TableStatus"]
        print(f"Successfully deleted table - {name}")
        print(f"Status - {status}\n")
    except ClientError as err:
        print(err)


@aws.command()
def create_bucket():
    """Create the single S3 bucket."""
    try:
        response = create_s3_bucket()
        print("Bucket successfully created!")
    except ClientError as err:
        print(err, "\n")


@aws.command()
def delete_bucket():
    """Delete the single S3 bucket."""
    try:
        response = delete_s3_bucket()
        print("Bucket successfully deleted!")
    except ClientError as err:
        print(err, "\n")


if __name__ == "__main__":
    aws()
