from flask import Blueprint, g, request, render_template
from app.extensions import socketio
from app.decorators.auth import socketio_jwt_required
from app.models import TokenType
from app.repositories import database_repository


sockets = Blueprint("sockets", __name__)


from app.sockets import private_chats, group_chats, messages


@socketio.on("connect")
@socketio_jwt_required(TokenType.ACCESS_TOKEN)
def connect_handler():
    """Establish a connection from the client to the server.
    The user's session is saved in the database for as long as the 
    connection is alive.
    """
    g.current_user.ping()
    g.current_user.socketio_session_id = request.sid
    g.current_user.add_room(request.sid)
    database_repository.update_user(
        g.current_user,
        {
            "socketio_session_id": g.current_user.socketio_session_id,
            "is_online": g.current_user.is_online,
            "last_seen_at": g.current_user.last_seen_at,
            "rooms": g.current_user.rooms
        },
    )
    print(f"{g.current_user.username} connected to server!")


@socketio.on("disconnect")
def disconnect_handler():
    """Remove the user's session id from the database and do any other
    necessary cleanup when the client disconnects from the server.
    """
    print("User disconnected from server!")
    g.current_user.is_online = False
    g.current_user.socketio_session_id = ""
    g.current_user.clear_rooms()
    database_repository.update_user(
        g.current_user,
        {
            "socketio_session_id": g.current_user.socketio_session_id,
            "is_online": g.current_user.is_online,
            "rooms": g.current_user.rooms,
        },
    )


@socketio.event
@socketio_jwt_required(TokenType.ACCESS_TOKEN)
def ping_user():
    """Clients must send this event periodically to keep the user online."""
    g.current_user.ping()
    database_repository.update_user(
        g.current_user, 
        {"is_online": g.current_user.is_online, "last_seen_at": g.current_user.last_seen_at}
    )


@sockets.route("/testing_chat")
def testing_chat():
    """Return a barebones template used to manually test the
    functionality of the socketio event handlers.
    """
    return render_template("chat.html")
