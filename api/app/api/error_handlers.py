"""This module contains error handlers for the api blueprint."""

from http import HTTPStatus
from app.api import api


@api.errorhandler(HTTPStatus.METHOD_NOT_ALLOWED)
def method_not_allowed(error):
    """Triggered when a request is made to an endpoint with
    an http method that is not allowed for that endpoint.
    """
    return (
        {
            "error": "Method not allowed for the requested endpoint",
            "status_code": HTTPStatus.METHOD_NOT_ALLOWED,
        },
        HTTPStatus.METHOD_NOT_ALLOWED,
    )


