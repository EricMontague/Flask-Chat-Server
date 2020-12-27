"""This file contains various cli commands for automating tasks
such as database table creation, running tests and more.
"""


import click
from aws_services_setup.utils import create_application_table, delete_application_table
from botocore.exceptions import ClientError



@click.group()
def dynamo_db():
    pass


@dynamo_db.command()
def create_table():
    """Create the single DynamoDB Users table"""
    try:
        table = create_application_table()
        print(f"Successfully created table - {table.table_name}")
        print(f"Status - {table.table_status}\n")
    except ClientError as err:
        print(err, "\n")


@dynamo_db.command()
def delete_table():
    """Delete the single Dynamodb table"""
    try:
        response = delete_application_table()
        name = response["TableDescription"]["TableName"]
        status = response["TableDescription"]["TableStatus"]
        print(f"Successfully deleted table - {name}")
        print(f"Status - {status}\n")
    except ClientError as err:
        print(err)
  
        

if __name__ == "__main__":
    dynamo_db()
