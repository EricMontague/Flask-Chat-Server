"""This module contains functions used to udpate models."""


from copy import deepcopy
from app.models.user import User
from app.models.image import Image, ImageType
from app.models.location import Location
from app.models.community import CommunityTopic


def update_user_model(old_user, updated_user_data):
    """Populate the given user model with new data."""
    updated_user = deepcopy(old_user)
    for attribute in updated_user_data:
        if attribute == "location":
            updated_user.location.state = updated_user_data["location"]["state"]
            updated_user.location.city = updated_user_data["location"]["city"]
            updated_user.location.country = updated_user_data["location"]["country"]
        else:
            setattr(updated_user, attribute, updated_user_data[attribute])
    return updated_user


def update_community_model(old_community, updated_community_data):
    """Populate the given community model with new data."""
    updated_community = deepcopy(old_community)
    for attribute in updated_community_data:
        if attribute == "location":
            updated_community.location.state = updated_community_data["location"]["state"]
            updated_community.location.city = updated_community_data["location"]["city"]
            updated_community.location.country = updated_community_data["location"]["country"]
        else:
            setattr(updated_community, attribute, updated_community_data[attribute])
    return updated_community
