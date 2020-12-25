"""This module holds view functions for accessing Community resources."""


from http import HTTPStatus
from flask import url_for, current_app
from app.api import api
from app.helpers.decorators import handle_request, handle_response
from app.schemas import (
    CommunitySchema,
    UrlParamsSchema,
    CommunityUrlParamsSchema,
    UserSchema,
)
from app.models.factories import CommunityFactory
from app.repositories import dynamodb_repository
from app.repositories.exceptions import DatabaseException, NotFoundException


@api.route("/communities")
@handle_request(CommunityUrlParamsSchema())
@handle_response(CommunitySchema(many=True))
def get_communities(url_params):
    """Return a list of community resources."""
    per_page = url_params.pop("per_page", current_app.config["RESULTS_PER_PAGE"])
    kwargs = {}
    if "next_cursor" in kwargs:
        kwargs["cursor"] = kwargs["next_cursor"]
    if "topic" in url_params:
        kwargs["topic"] = url_params["topic"].name
    else:
        kwargs.update(url_params)
    results = dynamodb_repository.get_communities(per_page, **kwargs)
    return results, HTTPStatus.OK


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


@api.route("/communities/<community_id>", methods=["PUT"])
@handle_request(CommunitySchema())
@handle_response(None)
def update_community(community_data, community_id):
    """Replace a community resource."""
    community = dynamodb_repository.get_community(community_id)
    if not community:
        return {"error": "Community not found"}, HTTPStatus.NOT_FOUND
    dynamodb_repository.update_community(community, community_data)
    return {}, HTTPStatus.NO_CONTENT


@api.route("/communities/<community_id>", methods=["DELETE"])
@handle_response(None)
def delete_community(community_id):
    """Delete a community resource."""
    community = dynamodb_repository.get_community(community_id)
    if not community:
        return {"error": "Community not found"}, HTTPStatus.NOT_FOUND
    dynamodb_repository.remove_community(community)
    return {}, HTTPStatus.NO_CONTENT


@api.route("/communities/<community_id>/members")
@handle_request(UrlParamsSchema())
@handle_response(UserSchema(many=True))
def get_community_members(url_params, community_id):
    """Return a list of users that belong to the given community."""
    per_page = url_params.get("per_page", current_app.config["RESULTS_PER_PAGE"])
    try:
        results = dynamodb_repository.get_community_members(community_id, per_page)
    except NotFoundException as err:
        return {"error": str(err)}, HTTPStatus.NOT_FOUND
    except DatabaseException as err:
        return {"error": str(err)}, HTTPStatus.BAD_REQUEST
    return results, HTTPStatus.OK


# What method should this be?
@api.route("/communities/<community_id>/members/<user_id>", methods=["PUT"])
@handle_response(None)
def join_community(community_id, user_id):
    """Add a new member to a community."""
    try:
        dynamodb_repository.add_community_member(community_id, user_id)
    except NotFoundException as err:
        return {"error": str(err)}, HTTPStatus.NOT_FOUND
    except DatabaseException as err:
        return {"error": str(err)}, HTTPStatus.BAD_REQUEST
    return {}, HTTPStatus.OK


# What method should this be?
@api.route("/communities/<community_id>/members/<user_id>", methods=["DELETE"])
@handle_response(None)
def leave_community(community_id, user_id):
    try:
        dynamodb_repository.remove_community_member(community_id, user_id)
    except NotFoundException as err:
        return {"error": str(err)}, HTTPStatus.NOT_FOUND
    except DatabaseException as err:
        return {"error": str(err)}, HTTPStatus.BAD_REQUEST
    return {}, HTTPStatus.NO_CONTENT
