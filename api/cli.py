"""This file contains various cli commands for automating tasks
such as database table creation, running tests and more.
"""


import click
from dynamo_utils import create_users_table, delete_table
from botocore.exceptions import ClientError


table_functions = {"users": create_users_table}


@click.group()
def dynamo_db():
    pass


@dynamo_db.command()
@click.argument("table_names", nargs=-1)
def create_tables(table_names):
    """Create Dynamodb tables."""
    if not table_names:
        for name, func in table_functions.items():
            try:
                table = func()
                print(f"Successfully created table - {name}")
                print(f"Status - {table.table_status}\n")
            except ClientError as err:
                print(err, "\n")
    else:
        invalid_names = []
        for name in table_names:
            if name.lower() not in table_functions:
                invalid_names.append(name)
            else:
                try:
                    func = table_functions[name.lower()]
                    table = func()
                    print(f"Created table: {name}, Status: {table.table_status}")
                except ClientError as err:
                    print(err, "\n")
        handle_invalid_table_names(invalid_names)


@dynamo_db.command()
@click.argument("table_name")
def delete_tables(table_name):
    """Delete Dynamodb tables."""
    if not table_name:
        print("Please provide a table name")
    elif table_name.lower() not in table_functions:
        print("Please provide a valid table name")
    else:
        try:
            response = delete_table(table_name.lower())
            name = response["TableDescription"]["TableName"]
            status = response["TableDescription"]["TableStatus"]
            print(f"Successfully deleted table - {name}")
            print(f"Status - {status}\n")
        except ClientError as err:
            print(err)


def handle_invalid_table_names(invalid_names):
    """Print invalid table names to the console."""
    if invalid_names:
        print("\nThe following table names were not recognized and were not created: ")
        for name in invalid_names:
            print(name)
        print("Please provide valid table names and try again")


if __name__ == "__main__":
    dynamo_db()
