"""This module contains helper functions for the sockets blueprint."""


from uuid import uuid4
from flask import g, url_for
from app.models import Notification, NotificationType
from app.schemas import NotificationSchema
from flask_socketio import emit


def send_group_chat_notifications(repo, chat_message, group_chat):
    """Create notifications for the newly created group chat message, store
    them in the database and emit to all clients in the socketio room.
    """
    limit = 25
    notification_schema = NotificationSchema()
    results = repo.get_group_chat_members(group_chat.community_id, group_chat.id, limit)
    for member in results["models"]:
        if member.id != g.current_user.id:
            notification = Notification(
                chat_message.timestamp.isoformat() + "-" + uuid4().hex,
                member.id,
                NotificationType.NEW_GROUP_CHAT_MESSAGE,
                f"{g.current_user.username} posted a new message in {group_chat.name}",
                url_for(
                    "api.get_group_chat_message",
                    group_chat_id=group_chat.id,
                    message_id=chat_message.id,
                ),
            )
            repo.add_user_notification(notification)
            if member.socketio_session_id:
                emit(
                    "new_notification",
                    notification_schema.dumps(notification),
                    room=member.socketio_session_id,
                )


def send_private_chat_notifications(repo, chat_message, private_chat):
    """Create notifications for the newly created private chat message, store
    them in the database and emit to other client in the room.
    """
    notification_schema = NotificationSchema()
    other_user = private_chat.get_other_user(g.current_user.id)
    notification = Notification(
        chat_message.timestamp.isoformat() + "-" + uuid4().hex,
        other_user.id,
        NotificationType.NEW_PRIVATE_CHAT_MESSAGE,
        f"{g.current_user.username} sent you a new message",
        url_for(
            "api.get_private_chat_message",
            private_chat_id=private_chat.id,
            message_id=chat_message.id,
        ),
    )
    repo.add_user_notification(notification)
    if other_user.socketio_session_id:
        emit(
            "new_notification",
            notification_schema.dumps(notification),
            room=other_user.socketio_session_id,
        )
