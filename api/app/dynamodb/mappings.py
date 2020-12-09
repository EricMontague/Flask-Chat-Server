"""This module contains functions and classes for mapping DynamoDB items to models.
"""


from datetime import datetime
from app.models import User, Role, RoleName, RolePermission, Location, Image, ImageType


def create_user_from_item(user_item):
    """Create and return a user model from a DynamoDB item."""
    # Remove uneeded attributes
    del user_item["SK"]
    del user_item["type"]
    user_id = user_item.pop("PK")["S"].split("#")[-1]
    user_attributes = {"id": user_id}
    for attribute_name, attribute_value in user_item.items():
        if attribute_name in {"avatar", "cover_photo"}:
            actual_value = create_image_from_map(user_item[attribute_name]["M"])
        elif attribute_name == "location":
            actual_value = create_location_from_map(user_item["location"]["M"])
        elif attribute_name == "role":
            actual_value = create_role_from_map(user_item["role"]["M"])
        elif attribute_name in {"last_seen_at", "created_at"}:
            actual_value = datetime.fromisoformat(attribute_value["S"])
        else:
            actual_value = list(user_item[attribute_name].values())[0]
        user_attributes[attribute_name] = actual_value
    password_hash = user_attributes.pop("password_hash")
    user = User(**user_attributes)
    user._password_hash = password_hash
    return user


def create_location_from_map(location_map):
    """Create and return a location model from a DynamoDB map."""
    location_attributes = {}
    for attribute_name, attribute_value in location_map.items():
        location_attributes[attribute_name] = attribute_value["S"]
    return Location(**location_attributes)


def create_role_from_map(role_map):
    """Create and return a role model from a DynamoDB map."""
    role_attributes = {}
    for attribute_name, attribute_value in role_map.items():
        if attribute_name == "name":
            actual_value = RoleName[attribute_value["S"]]
        elif attribute_name == "permissions":
            actual_value = {RolePermission[perm] for perm in attribute_value["SS"]}
        role_attributes[attribute_name] = actual_value
    return Role(**role_attributes)


def create_image_from_map(image_map):
    """Create and return an image model from a DynamoDB map."""
    image_attributes = {}
    for attribute_name, attribute_value in image_map.items():
        if attribute_name in {"width", "height"}:
            actual_value = int(attribute_value["N"])
        elif attribute_name == "image_type":
            actual_value = ImageType[attribute_value["S"]]
        elif attribute_name == "uploaded_at":
            actual_value = datetime.fromisoformat(attribute_value["S"])
        else:
            actual_value = attribute_value["S"]
        image_attributes[attribute_name] = actual_value
    return Image(**image_attributes)

