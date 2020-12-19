"""This module contains decorators to be used through the application."""


import functools
from http import HTTPStatus
from flask import request, make_response
from marshmallow import ValidationError


def handle_get_request(schema, url_params):
    """Validate query string parameters sent on a GET request."""
    try:
        return schema.load(url_params)
    except ValidationError as err:
        return {"error": err.messages["_schema"]}, HTTPStatus.UNPROCESSABLE_ENTITY
    

def handle_post_and_put_requests(schema, json_data):
    """Validate and return deserialized JSON body of POST and PUT requests."""
    try:
        return schema.load(json_data)
    except ValidationError as err:
        if "_schema" in err.messages:
            return (
                {"error": err.messages["_schema"]},
                HTTPStatus.UNPROCESSABLE_ENTITY,
            )
        return {"errors": err.messages}, HTTPStatus.UNPROCESSABLE_ENTITY


def handle_request(schema):
    """Decorator to handle deserializing the JSON body
    of requests to API routes as well as Url parameters.
    Meant to only be used on GET, PUT, and POST requests
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if request.method == "GET":
                view_argument = handle_get_request(schema, request.args)
            elif request.method in {"POST", "PUT"}:
                if not request.json:
                    return (
                        {"error": "Missing JSON Body in request"},
                        HTTPStatus.BAD_REQUEST,
                    )
                view_argument = handle_post_and_put_requests(schema, request.json)
            if "error" in view_argument or "errors" in view_argument:
                return view_argument
            return func(view_argument, *args, **kwargs)
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
            if (
                not schema
                or isinstance(results, str)
                or isinstance(results, dict)
                and (not results or "error" in results or "errors" in results)
            ):
                api_response = make_response(results, http_status_code)
            elif isinstance(results, list):  # attempt to serialize list
                serialized_results = schema.dump(results)
                api_response = make_response(
                    serialized_results or results, http_status_code
                )
            elif isinstance(results, dict):  # attempt to serialize every item in dict
                for key in results:
                    if key == "model":
                        model = results.pop(key)
                        resource_name = schema.COLLECTION_NAME[:-1]
                        results[resource_name] = schema.dump(model)
                    elif key == "models":
                        models = results.pop(key)
                        results[schema.COLLECTION_NAME] = schema.dump(models)
                api_response = make_response(results, http_status_code)
            else:  # assume it's a model
                api_response = make_response(schema.dump(results), http_status_code)

            if len(view_response) == 3:  # extra headers are included
                api_response.headers.extend(view_response[2])
            api_response.headers["Content-Type"] = "application/json"
            return api_response

        return wrapper

    return decorator

