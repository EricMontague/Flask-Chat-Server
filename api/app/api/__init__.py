"""This package contains all of the routes for the api blueprint."""


from flask import Blueprint


api = Blueprint("api", __name__)


from app.api import users, communities, private_chats, group_chats, admin
