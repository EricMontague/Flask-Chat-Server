"""This module contains a simple factory class to abstract away the
creation of community objects.
"""


from uuid import uuid4
from copy import deepcopy
from app.models import (
    Community,
    CommunityTopic,
    Location,
    Image
)
from app.models.image import default_community_avatar, default_community_cover_photo


class CommunityFactory:
    """Class to create community objects."""


    @staticmethod
    def create_community(community_data):
        """Return a new Community model."""
        community_data_copy = deepcopy(community_data)
        community_data_copy["id"] = uuid4().hex
        community_data_copy["location"] = Location(**community_data_copy.pop("location"))
        community = Community(
            **community_data_copy,
            avatar=default_community_avatar,
            cover_photo=default_community_cover_photo
        )
        return community