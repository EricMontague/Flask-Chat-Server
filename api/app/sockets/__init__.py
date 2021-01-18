from flask import Blueprint, g, request, render_template
from app.extensions import socketio
from app.decorators.auth import socketio_jwt_required
from app.models import TokenType
from app.repositories import dynamodb_repository


sockets = Blueprint("sockets", __name__)


from app.sockets import private_chats, group_chats, messages


@socketio.on("connect")
@socketio_jwt_required(TokenType.ACCESS_TOKEN)
def connect_handler():
    """Establish a connection from the client to the server.
    The user's session is saved in the database for as long as the 
    connection is alive.
    """
    dynamodb_repository.update_user(
        g.current_user, {"socketio_session_id": request.sid, "is_online": True}
    )
    print(f"{g.current_user.username} connected to server!")


@socketio.on("disconnect")
def disconnect_handler():
    """Remove the user's session id from the database and do any other
    necessary cleanup when the client disconnects from the server.
    """
    dynamodb_repository.update_user(
        g.current_user, {"socketio_session_id": "", "is_online": False}
    )


@sockets.route("/testing_chat")
def testing_chat():
    return render_template("chat.html")
