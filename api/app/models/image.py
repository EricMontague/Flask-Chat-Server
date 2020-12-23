"""This module contains the image model."""


from uuid import uuid4
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
    uploaded_at: datetime = datetime.now()


class ImageType(Enum):
    """Enum to represent image types."""

    USER_PROFILE_PHOTO = 1
    USER_COVER_PHOTO = 2
    COMMUNITY_PROFILE_PHOTO = 3
    COMMUNITY_COVER_PHOTO = 4


class DefaultImageUrl:
    """Class to represent default image urls."""

    USER_PROFILE_PHOTO = "https://www.mycdn/2323g34y34"
    USER_COVER_PHOTO = "https://www.mycdn/qwtkqw98"
    COMMUNITY_PROFILE_PHOTO = "https://www.mycdn/v346231235"
    COMMUNITY_COVER_PHOTO = "https://www.mycdn/sek98335"


default_user_avatar = Image(
    uuid4().hex,
    ImageType.USER_PROFILE_PHOTO,
    DefaultImageUrl.USER_PROFILE_PHOTO,
    200,
    200,
)
default_user_cover_photo = Image(
    uuid4().hex, ImageType.USER_COVER_PHOTO, DefaultImageUrl.USER_COVER_PHOTO, 400, 500
)
default_community_avatar = Image(
    uuid4().hex,
    ImageType.COMMUNITY_PROFILE_PHOTO,
    DefaultImageUrl.COMMUNITY_PROFILE_PHOTO,
    200,
    200,
)
default_community_cover_photo = Image(
    uuid4().hex,
    ImageType.COMMUNITY_COVER_PHOTO,
    DefaultImageUrl.COMMUNITY_COVER_PHOTO,
    400,
    500,
)
