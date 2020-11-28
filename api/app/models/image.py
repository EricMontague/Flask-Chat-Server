"""This module contains the image model."""


from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Image:
    """Class to represent an image."""

    id: str
    image_type: str
    url: str
    height: int
    width: int



class ImageType:
    """Class to represent image types."""

    USER_PROFILE_IMAGE = "user_profile_image"
    USER_COVER_IMAGE = "user_cover_image"
    COMMUNITY_PROFILE_IMAGE = "community_profile_image"
    COMMUNITY_COVER_IMAGE = "community_cover_image"

    
