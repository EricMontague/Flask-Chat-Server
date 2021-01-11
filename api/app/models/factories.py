"""This module contains simple factories for creating models."""


from uuid import uuid4
from copy import deepcopy
from app.models import (
    User,
    Role,
    RoleName,
    RolePermission,
    Location,
    Image,
    Community,
    CommunityTopic,
)
from app.models.image import (
    default_community_avatar,
    default_community_cover_photo,
    default_user_avatar,
    default_user_cover_photo,
)
from app.models.role import regular_user_role


class UserFactory:
    """Class to create user objects."""

    @staticmethod
    def create_user(user_data):
        """Return a new user model."""
        user_data_copy = deepcopy(user_data)
        user_data_copy["id"] = uuid4().hex
        user_data_copy["role"] = regular_user_role
        user_data_copy["location"] = Location(**user_data_copy.pop("location"))
        password = user_data_copy.pop("password")
        user = User(
            **user_data_copy,
            avatar=default_user_avatar,
            cover_photo=default_user_cover_photo
        )
        user.password = password
        return user


class CommunityFactory:
    """Class to create community objects."""

    @staticmethod
    def create_community(community_data):
        """Return a new Community model."""
        community_data_copy = deepcopy(community_data)
        community_data_copy["id"] = uuid4().hex
        community_data_copy["location"] = Location(
            **community_data_copy.pop("location")
        )
        community = Community(
            **community_data_copy,
            avatar=default_community_avatar,
            cover_photo=default_community_cover_photo
        )
        return community
