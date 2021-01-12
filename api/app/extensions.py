"""This module contains the Flask extensions for the application."""


from flask_bcrypt import Bcrypt
from flask_marshmallow import Marshmallow
from flask_socketio import SocketIO


bcrypt = Bcrypt()
ma = Marshmallow()
socketio = SocketIO(logger=True, engineio_logger=True)

