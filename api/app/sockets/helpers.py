"""This module contains helper functions for the sockets blueprint."""


from uuid import uuid4
from flask import url_for
from app.models import Notification, NotificationType
from app.schemas import NotificationSchema
from app.repositories import database_repository
from flask_socketio import emit


def send_group_chat_notifications(target_url, current_user, chat_message, group_chat):
    """Create notifications for the newly created group chat message, store
    them in the database and emit to all clients in the socketio room.
    """
   
    limit = 25
    notification_schema = NotificationSchema()
    results = database_repository.get_group_chat_members(group_chat.community_id, group_chat.id, limit)
    for member in results["models"]:
        if member.id != current_user.id:
            notification = Notification(
                chat_message.timestamp.isoformat() + "-" + uuid4().hex,
                member.id,
                NotificationType.NEW_GROUP_CHAT_MESSAGE,
                f"{current_user.username} posted a new message in {group_chat.name}",
                target_url
            )
            database_repository.add_user_notification(notification)
            
            if member.socketio_session_id:
                emit(
                    "new_notification",
                    notification_schema.dumps(notification),
                    room=member.socketio_session_id,
                )


def send_private_chat_notifications(target_url, current_user, chat_message, private_chat):
    """Create notifications for the newly created private chat message, store
    them in the database and emit to other client in the room.
    """
    
    notification_schema = NotificationSchema()
    other_user = private_chat.get_other_user(current_user.id)
    notification = Notification(
        chat_message.timestamp.isoformat() + "-" + uuid4().hex,
        other_user.id,
        NotificationType.NEW_PRIVATE_CHAT_MESSAGE,
        f"{current_user.username} sent you a new message",
        target_url
    )
    database_repository.add_user_notification(notification)
    
    if other_user.socketio_session_id:
        emit(
            "new_notification",
            notification_schema.dumps(notification),
            room=other_user.socketio_session_id,
        )
