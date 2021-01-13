"""This package contains all of the routes for the api blueprint."""


from flask import Blueprint
from app.decorators.auth import jwt_required
from app.models import TokenType


api = Blueprint("api", __name__)


@api.before_request
@jwt_required(TokenType.ACCESS_TOKEN)
def authentication_hook():
    """Request hook that makes sure every request to 
    the api is authenticated with a JWT.
    """
    return None
    

from app.api import users, communities, private_chats, group_chats, admin
