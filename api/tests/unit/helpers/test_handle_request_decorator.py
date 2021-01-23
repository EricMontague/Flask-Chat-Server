"""This file contains tests for the handle_request decorator as well as the
functions that it depends on.
"""


import pytest
from http import HTTPStatus
from app.decorators.views import handle_request, handle_get_request, handle_post_or_put_request
from marshmallow import ValidationError
from unittest.mock import patch, create_autospec


def test_handle_get_request_invalid_parameters_returns_errors(fake_error_schema_class):
    """Test that when a schema is passed in and its load method raises a ValidationError
    that a dictionary with the error is returned.
    """
    fake_error_schema = fake_error_schema_class()
    url_params = {"next": "next cursor", "per_page": 12}
    error = handle_get_request(fake_error_schema, url_params)
    assert "error" in error


def test_handle_get_request_valid_parameters_returns_data(fake_data_schema):
    """Test that when the load method of a schema doesn't throw an error,
    that data is returned.
    """
    url_params = {"next": "next cursor", "per_page": 12}
    results = handle_get_request(fake_data_schema, url_params)
    assert "next" in results
    assert "per_page" in results


def test_handle_post_put_request_invalid_parameters_schema_error(
    fake_error_schema_class,
):
    """Test that when a schema is passed in and its load method raises a ValidationError
    caused by a schema level error that a dictionary with that error is returned.
    """
    fake_error_schema = fake_error_schema_class()
    fake_data = {"username": "Brad12", "age": 12}
    error = handle_post_or_put_request(fake_error_schema, fake_data)
    assert "error" in error


def test_handle_post_put_request_invalid_parameters_field_errors(
    fake_error_schema_class,
):
    """Test that when a schema is passed in and its load method raises a ValidationError
    caused by a field level validator that a dictionary with that error is returned.
    """
    fake_error_schema = fake_error_schema_class("random_field")
    fake_data = {"username": "Brad12", "age": 12}
    errors = handle_post_or_put_request(fake_error_schema, fake_data)
    assert "errors" in errors


def test_handle_post_put_request_valid_parameters_field_errors(fake_data_schema):
    """Test that when the load method of a schema doesn't throw an error,
    that data is returned.
    """
    fake_data = {"username": "Brad12", "age": 12}
    results = handle_get_request(fake_data_schema, fake_data)
    assert "username" in results
    assert "age" in results


@patch("app.decorators.views.handle_get_request", autospec=True)
@patch("app.decorators.views.request")
def test_handle_request_decorator_get_request(
    mock_request_context, mock_handle_get_request, fake_data_schema
):
    """Test to confirm that if the HTTP method is GET, that the handle_get_request()
    function is called and its return value is passed to the Flask view function.
    """
    # Setup mocks
    mock_request_context.method = "GET"
    mock_request_context.args = "Get request handler "
    mock_handle_get_request.return_value = mock_request_context.args

    # Setup decorator
    fake_view_function = lambda string1, string2: string1 + string2
    decorator_function = handle_request(fake_data_schema)
    wrapper_function = decorator_function(fake_view_function)

    assert wrapper_function("was called!") == "Get request handler was called!"


@patch("app.decorators.views.handle_post_or_put_request", auto_spec=True)
@patch("app.decorators.views.request")
def test_handle_request_decorator_post_request(
    mock_request_context, mock_handle_post_or_put_request, fake_data_schema
):
    """Test to confirm that if the HTTP method is POST, that the handle_post_or_put_request()
    function is called and its return value is passed to the Flask view function.
    """
    # Setup decorator
    fake_view_function = lambda user_dict: user_dict.pop("name")
    decorator_function = handle_request(fake_data_schema)
    wrapper_function = decorator_function(fake_view_function)

    # Setup mocks for POST request
    mock_request_context.method = "POST"
    mock_request_context.json = {"name": "Kenny"}
    mock_handle_post_or_put_request.return_value = mock_request_context.json

    assert wrapper_function() == "Kenny"
    mock_handle_post_or_put_request.assert_called_with(
        fake_data_schema, mock_request_context.json
    )


@patch("app.decorators.views.handle_post_or_put_request", auto_spec=True)
@patch("app.decorators.views.request")
def test_handle_request_decorator_put_request(
    mock_request_context, mock_handle_post_or_put_request, fake_data_schema
):
    """Test to confirm that if the HTTP method is PUT, that the handle_post_or_put_request()
    function is called and its return value is passed to the Flask view function.
    """

    # Setup decorator
    fake_view_function = lambda user_dict: user_dict.pop("name")
    decorator_function = handle_request(fake_data_schema)
    wrapper_function = decorator_function(fake_view_function)

    # Setup mocks for PUT request
    mock_request_context.method = "PUT"
    mock_request_context.json = {"name": "Brad"}
    mock_handle_post_or_put_request.return_value = mock_request_context.json

    assert wrapper_function() == "Brad"
    mock_handle_post_or_put_request.assert_called_with(
        fake_data_schema, mock_request_context.json
    )


@patch("app.decorators.views.request")
def test_handle_request_decorator_post_request_no_json_body_returns_error(
    mock_request_context, fake_data_schema
):
    """Test that confirms that the view function isn't called when no JSON
    body is present on a POST request and instead a dictionary with an error message is returned.
    """

    # Setup decorator
    mock_view_function = create_autospec(lambda user_dict: user_dict.pop("name"))
    decorator_function = handle_request(fake_data_schema)
    wrapper_function = decorator_function(mock_view_function)

    # Setup mocks
    mock_request_context.method = "POST"
    mock_request_context.json = None

    # Assertions
    error, http_status_code = wrapper_function()
    assert error == {"error": "Missing JSON Body in request"}
    assert http_status_code == HTTPStatus.BAD_REQUEST
    mock_view_function.assert_not_called()


@patch("app.decorators.views.request")
def test_handle_request_decorator_put_request_no_json_body_returns_error(
    mock_request_context, fake_data_schema
):
    """Test that confirms that the view function isn't called when no JSON
    body is present on a PUT request and instead a dictionary with an error message is returned.
    """

    # Setup decorator
    mock_view_function = create_autospec(lambda user_dict: user_dict.pop("name"))
    decorator_function = handle_request(fake_data_schema)
    wrapper_function = decorator_function(mock_view_function)

    # Setup mocks
    mock_request_context.method = "PUT"
    mock_request_context.json = None
    
    # Assertions
    error, http_status_code = wrapper_function()
    assert error == {"error": "Missing JSON Body in request"}
    assert http_status_code == HTTPStatus.BAD_REQUEST
    mock_view_function.assert_not_called()


@patch("app.decorators.views.handle_get_request")
@patch("app.decorators.views.request")
def test_handle_request_decorator_error_with_deserialization(
    mock_request_context, mock_handle_get_request, fake_data_schema
):
    """Test that confirms that if either handle_get_request() or
    handle_post_or_put_request() return a dictionary of errors,
    that those errors are returned and the view function is not called.
    """

    # Setup decorator
    mock_view_function = create_autospec(lambda user_dict: user_dict.pop("name"))
    decorator_function = handle_request(fake_data_schema)
    wrapper_function = decorator_function(mock_view_function)


    # Setup mocks
    mock_request_context.method = "GET"
    mock_handle_get_request.return_value = {"error": "Validation error occurred"}
    

    # Assertions
    error, http_status_code = wrapper_function()
    assert error == mock_handle_get_request.return_value
    assert http_status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    mock_view_function.assert_not_called()

    # Change the key of the dictionary. Should still see the same result
    mock_handle_get_request.reset_mock(return_value=True)
    mock_handle_get_request.return_value = {"errors": "Validation error occurred"}

    # Assertions again
    error, http_status_code = wrapper_function()
    assert error == mock_handle_get_request.return_value
    assert http_status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    mock_view_function.assert_not_called()
