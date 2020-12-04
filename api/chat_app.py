"""This file is the entrypoint for the application."""


import os
from app import create_app
from app.models import (
    ChatRequest,
    ChatRequestStatus,
    PrivateChat,
    GroupChat,
    Community,
    CommunityTopic,
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
from app.repositories import dynamodb_repository


app = create_app(os.environ.get("FLASK_CONFIG", "development"))


@app.shell_context_processor
def make_shell_context():
    """Allow models and other objects to be globally
    accessible in the Flask shell.
    """
    return dict(
        dynamodb_repository=dynamodb_repository,
        dynamodb_client=dynamodb_client,
        ChatRequest=ChatRequest,
        ChatRequestStatus=ChatRequestStatus,
        PrivateChat=PrivateChat,
        GroupChat=GroupChat,
        Community=Community,
        CommunityTopic=CommunityTopic,
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
    app.run(debug=True)
