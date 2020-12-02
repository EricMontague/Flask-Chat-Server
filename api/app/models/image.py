"""This module contains the image model."""


from enum import Enum
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


class ImageType(Enum):
    """Enum to represent image types."""

    USER_PROFILE_PHOTO = 0
    USER_COVER_PHOTO = 1
    COMMUNITY_PROFILE_PHOTO = 2
    COMMUNITY_COVER_PHOTO = 3

