"""This package contains Marshmallow scheams used for serializing and
deserializing models.
"""


from app.schemas.user import UserSchema
from app.schemas.location import LocationSchema
from app.schemas.image import ImageSchema
from app.schemas.url_parameters import UrlParamsSchema, CommunityUrlParamsSchema, GroupChatUrlParamsSchema
from app.schemas.community import CommunitySchema
from app.schemas.notification import NotificationSchema
from app.schemas.message import PrivateChatMessageSchema, GroupChatMessageSchema, MessageSchema, ReactionSchema
from app.schemas.private_chat import PrivateChatSchema
from app.schemas.group_chat import GroupChatSchema
from app.schemas.role import RoleSchema
