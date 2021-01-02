"""This file is the entrypoint for the application."""


import os
from http import HTTPStatus
from app.extensions import socketio
from app import create_app
from app.models import (
    PrivateChat,
    GroupChat,
    Community,
    CommunityTopic,
    CommunityMembership,
    Image,
    ImageType,
    Message,
    Reaction,
    Notification,
    NotificationType,
    Role,
    RolePermission,
    RoleName,
    User,
    Location,
)
from app.clients import dynamodb_client
from app.repositories import dynamodb_repository, s3_repository
from flask import jsonify

app = create_app(os.environ.get("FLASK_CONFIG", "development"))


# Blueprints can't handle 404 errors since this error occurs at the routing
# level before the blueprint is determined
@app.errorhandler(HTTPStatus.NOT_FOUND)
def resource_not_found(error):
    """Triggered when a requested resource could not
    be found.
    """
    return (
        {
            "error": "The requested resource could not be found",
            "status_code": HTTPStatus.NOT_FOUND,
        },
        HTTPStatus.NOT_FOUND,
    )


@app.errorhandler(HTTPStatus.INTERNAL_SERVER_ERROR)
def internal_server_error(error):
    """Triggered as a means of last resort when a specific
    error on the server is not caught.
    """
    return (
        {
            "error": "Due to an internal server error, we could not process your request",
            "status_code": HTTPStatus.INTERNAL_SERVER_ERROR,
        },
        HTTPStatus.INTERNAL_SERVER_ERROR,
    )


@app.shell_context_processor
def make_shell_context():
    """Allow models and other objects to be globally
    accessible in the Flask shell.
    """
    return dict(
        dynamodb_repository=dynamodb_repository,
        dynamodb_client=dynamodb_client,
        s3_repository=s3_repository,
        PrivateChat=PrivateChat,
        GroupChat=GroupChat,
        Community=Community,
        CommunityTopic=CommunityTopic,
        CommunityMembership=CommunityMembership,
        Image=Image,
        ImageType=ImageType,
        Message=Message,
        Reaction=Reaction,
        Notification=Notification,
        NotificationType=NotificationType,
        Role=Role,
        RolePermission=RolePermission,
        RoleName=RoleName,
        User=User,
        Location=Location,
    )


if __name__ == "__main__":
    socketio.run(app)
