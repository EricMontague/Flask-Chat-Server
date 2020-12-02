"""This file contains various cli commands for automating tasks
such as database table creation, running tests and more.
"""


import click
from dynamo_utils import (
    create_users_table,
    create_communities_table,
    create_group_chats_table,
    create_private_chats_table,
    create_notifications_table,
    create_chat_requests_table,
    delete_table
)
from botocore.exceptions import ClientError


create_table_functions = {
    "users": create_users_table,
    "communities": create_communities_table,
    "group_chats": create_group_chats_table,
    "private_chats": create_private_chats_table,
    "notifications": create_notifications_table,
    "chat_requests": create_chat_requests_table
}


@click.group()
def dynamo_db():
    pass


@dynamo_db.command()
@click.argument("table_names", nargs=-1)
def create_tables(table_names):
    """Create Dynamodb tables."""
    if not table_names:
        for name, func in create_table_functions.items():
            try:
                table = func()
                print(f"Successfully created table - {name}")
                print(f"Status - {table.table_status}\n")
            except ClientError as err:
                print(err, "\n")
    else:
        invalid_names = []
        for name in table_names:
            snaked_cased_name = name.lower().replace(" ", "_")
            if snaked_cased_name not in create_table_functions:
                invalid_names.append(name)
            else:
                try:
                    func = create_table_functions[snaked_cased_name]
                    table = func()
                    print(f"Created table: {table.table_name}, Status: {table.table_status}")
                except ClientError as err:
                    print(f"\nTableName: {name}")
                    print(err, "\n")
        handle_invalid_table_names(invalid_names)


@dynamo_db.command()
@click.argument("table_names", nargs=-1)
def delete_tables(table_names):
    """Delete Dynamodb tables."""
    if not table_names:
        for name in create_table_functions:
            camel_cased_name = name.title().replace("_", "")
            try:
                response = delete_table(camel_cased_name)
                name = response["TableDescription"]["TableName"]
                status = response["TableDescription"]["TableStatus"]
                print(f"Successfully deleted table - {name}")
                print(f"Status - {status}\n")
            except ClientError as err:
                print(err)
    else:
        invalid_names = []
        for name in table_names:
            snaked_cased_name = name.lower().replace(" ", "_")
            if snaked_cased_name not in create_table_functions:
                invalid_names.append(name)
            else:
                camel_cased_name = name.title().replace(" ", "")
                try:
                    response = delete_table(camel_cased_name)
                    name = response["TableDescription"]["TableName"]
                    status = response["TableDescription"]["TableStatus"]
                    print(f"Successfully deleted table - {name}")
                    print(f"Status - {status}\n")
                except ClientError as err:
                    print(err)
        handle_invalid_table_names(invalid_names)
        

def handle_invalid_table_names(invalid_names):
    """Print invalid table names to the console."""
    if invalid_names:
        print("\nThe following table names were not recognized and were not created: ")
        for name in invalid_names:
            print(name)
        print("Please provide valid table names and try again")


if __name__ == "__main__":
    dynamo_db()
