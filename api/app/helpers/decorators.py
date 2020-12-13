"""This module contains decorators to be used through the application."""


import functools
from http import HTTPStatus
from flask import request, make_response
from marshmallow import ValidationError


def handle_request(schema):
    """Decorator to handle deserializing the JSON body
    of requests to API routes.
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            request_data = request.json
            if not request_data:
                return (
                    {"message": "Missing JSON Body in request"},
                    HTTPStatus.BAD_REQUEST,
                )
            try:
                model_dict = schema.load(request_data)
            except ValidationError as err:
                return {"errors": err.messages}, HTTPStatus.UNPROCESSABLE_ENTITY
            return func(model_dict, *args, **kwargs)

        return wrapper

    return decorator


def handle_response(schema):
    """Decorator to handle serializing models to JSON
    responses for API routes.
    """

    def decorator(view_func):
        @functools.wraps(view_func)
        def wrapper(*args, **kwargs):
            view_response = view_func(*args, **kwargs)
            # view_response is a tuple in the form of (results, http_status_code, headers)
            # or (results, http_status_code)
            results = view_response[0]
            http_status_code = view_response[1]
            if not schema or isinstance(results, dict) and (not results or "error" in results):
                api_response = make_response(results, http_status_code)
            else:
                api_response = make_response(schema.dump(results), http_status_code)

            if len(view_response) == 3:  # extra headers are included
                api_response.headers.extend(view_response[2])
            api_response.headers["Content-Type"] = "application/json"
            return api_response

        return wrapper

    return decorator


def handle_query_params(func):
    """Decorator to handle parsing query parameters sent
    during a request to the api. It handles pagination, filtering, and sorting 
    for collections. The expected response from the decorated route is a
    an object that implements the AbstractDatabaseRepository interface."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        params = request.args
        return func(params, *args, **kwargs)

    return wrapper
