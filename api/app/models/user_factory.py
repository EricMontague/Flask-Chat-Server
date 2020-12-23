"""This module contains a simple factory class to abstract away the 
creation of user objects.
"""


from uuid import uuid4
from copy import deepcopy
from app.models import (
    User,
    Role,
    RoleName,
    RolePermission,
    CommunityPermission,
    Location,
    Image,
)
from app.models.image import default_user_avatar, default_user_cover_photo


class UserFactory:
    """Class to create user objects."""

    @staticmethod
    def create_user(user_data):
        """Return a new user model."""
        user_data_copy = deepcopy(user_data)
        user_data_copy["id"] = uuid4().hex
        permissions = {
            perm for perm in RolePermission if perm != RolePermission.BAN_USERS
        }
        role = Role(RoleName.REGULAR_USER, permissions)
        user_data_copy["role"] = role
        user_data_copy["location"] = Location(**user_data_copy.pop("location"))
        password = user_data_copy.pop("password")
        user = User(
            **user_data_copy,
            avatar=default_user_avatar,
            cover_photo=default_user_cover_photo
        )
        user.password = password
        return user

