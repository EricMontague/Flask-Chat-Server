"""This file contains various cli commands for automating tasks
such as database table creation, running tests and more.
"""


import click
from dynamodb_setup.utils import create_users_table, delete_users_table
from botocore.exceptions import ClientError



@click.group()
def dynamo_db():
    pass


@dynamo_db.command()
def create_table():
    """Create the single DynamoDB Users table"""
    try:
        table = create_users_table()
        print(f"Successfully created table - {table.table_name}")
        print(f"Status - {table.table_status}\n")
    except ClientError as err:
        print(err, "\n")


@dynamo_db.command()
def delete_table(table_names):
    """Delete the single Dynamodb table"""
    try:
        response = delete_table("Users")
        name = response["TableDescription"]["TableName"]
        status = response["TableDescription"]["TableStatus"]
        print(f"Successfully deleted table - Users")
        print(f"Status - {status}\n")
    except ClientError as err:
        print(err)
  
        

if __name__ == "__main__":
    dynamo_db()
