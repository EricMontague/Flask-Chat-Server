"""This module holds view functions for accessing Community resources."""


from http import HTTPStatus
from flask import url_for
from app.api import api
from app.helpers.decorators import handle_request, handle_response
from app.schemas import CommunitySchema
from app.models.community_factory import CommunityFactory
from app.repositories import dynamodb_repository
from app.repositories.exceptions import DatabaseException


@api.route("/communities")
def get_communities():
    pass


@api.route("/communities")
def get_communities_by_topic():
    pass


@api.route("/communities")
def get_communities_by_location():
    pass


@api.route("/communities/<community_id>/members")
def get_community_members():
    pass


@api.route("/communities/<community_id>")
@handle_response(CommunitySchema())
def get_community(community_id):
    """Get a community resource."""
    community = dynamodb_repository.get_community(community_id)
    if not community:
        return {"error": "Community not found"}, HTTPStatus.NOT_FOUND
    return community, HTTPStatus.OK


@api.route("/communities", methods=["POST"])
@handle_request(CommunitySchema())
@handle_response(CommunitySchema())
def create_community(community_data):
    """Create a new community resource."""
    community = CommunityFactory.create_community(community_data)
    try:
        dynamodb_repository.add_community(community, "RandomUserIdForNow")
    except DatabaseException as err:
        return {"error": str(err)}, HTTPStatus.BAD_REQUEST
    headers = {"Location": url_for("api.get_community", community_id=community.id)}
    return (community, HTTPStatus.CREATED, headers)


@api.route("/communites/<community_id>", methods=["PUT"])
def update_community(community_data, community_id):
    pass


@api.route("/communities/<community_id>", methods=["DELETE"])
def delete_community(community_id):
    pass


# What method should this be?
@api.route("/communities/<community_id>", methods=["PUT"])
def join_community():
    pass


# What method should this be?
@api.route("/communities/<community_id>", methods=["PUT"])
def leave_community():
    pass
