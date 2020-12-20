"""This file contains tests for the handle response decorator
as well as the functions it depends on.
"""


import pytest
from http import HTTPStatus
from unittest.mock import patch, create_autospec
from app.helpers.decorators import (
    not_require_serialization,
    handle_response,
    handle_serialization,
    serialize_model_or_models
)


@patch("app.helpers.decorators.make_response")
@patch("app.helpers.decorators.handle_serialization")
@patch("app.helpers.decorators.not_require_serialization")
def test_handle_response_doesnt_require_serialization(
    mock_not_require_serialization,
    mock_handle_serialization,
    mock_make_response,
    fake_response,
    fake_data_schema,
):
    """Test to confirm that if the not_require_serialization function
    returns True that the handle_serialization function isn't called.
    """

    # Setup mocks
    mock_view_function = create_autospec(lambda arg: arg)
    mock_not_require_serialization.return_value = True
    mock_make_response.return_value = fake_response

    # Setup decorator
    decorator_function = handle_response(fake_data_schema)
    wrapper_function = decorator_function(mock_view_function)

    # Assertions
    view_argument = "Mock view called!"
    flask_response = wrapper_function(view_argument)
    assert flask_response.headers["Content-Type"] == "application/json"
    assert flask_response.status_code == HTTPStatus.OK
    assert flask_response.data == fake_response.data

    mock_view_function.assert_called_with(view_argument)
    mock_handle_serialization.assert_not_called()
    mock_make_response.assert_called()


@patch("app.helpers.decorators.make_response")
@patch("app.helpers.decorators.handle_serialization")
@patch("app.helpers.decorators.not_require_serialization")
def test_handle_response_does_require_serialization(
    mock_not_require_serialization,
    mock_handle_serialization,
    mock_make_response,
    fake_response,
    fake_data_schema,
):
    """Test to confirm that if the not_require_serialization function
    returns False that the handle_serialization function is called.
    """

    # Setup mocks
    mock_view_function = create_autospec(lambda arg: arg)
    mock_not_require_serialization.return_value = False
    mock_handle_serialization.return_value = fake_response

    # Setup decorator
    decorated_function = handle_response(fake_data_schema)
    wrapper_function = decorated_function(mock_view_function)

    # Assertions
    view_argument = "Mock view function called!"
    flask_response = wrapper_function(view_argument)

    assert flask_response.status_code == HTTPStatus.OK
    assert flask_response.headers["Content-Type"] == "application/json"
    assert flask_response.data == fake_response.data

    mock_view_function.assert_called_with(view_argument)
    mock_handle_serialization.assert_called()
    mock_make_response.assert_not_called()


@patch("app.helpers.decorators.make_response")
@patch("app.helpers.decorators.handle_serialization")
@patch("app.helpers.decorators.not_require_serialization")
def test_handle_response_extra_headers_present(
    mock_not_require_serialization,
    mock_handle_serialization,
    mock_make_response,
    fake_response,
    fake_data_schema,
):
    """Test that of the view function returns a tuple of length 3, that
    the extra headers are added to the flask response headers.
    """

    # Setup mocks
    fake_view_function = lambda arg: (
        arg,
        HTTPStatus.OK,
        {"Location": "https://api.github/users/123"},
    )
    mock_not_require_serialization.return_value = True
    mock_make_response.return_value = fake_response

    # Setup decorator
    decorator_function = handle_response(fake_data_schema)
    wrapper_function = decorator_function(fake_view_function)

    # Assertions
    view_argument = "Mock view function called!"
    flask_response = wrapper_function(view_argument)

    assert flask_response.status_code == HTTPStatus.OK
    assert flask_response.headers["Content-Type"] == "application/json"
    assert flask_response.headers["Location"] == "https://api.github/users/123"
    assert flask_response.data == fake_response.data


@pytest.mark.parametrize(
    "test_input, use_schema",
    [
        ("test with no schema", False),
        ("Hello World", True),
        ({"error": "Not user found"}, True),
        ({}, True),
        ({"errors": ["Error1", "Error2"]}, True),
    ],
)
def test_not_require_serialization_returns_true(
    test_input, use_schema, fake_data_schema
):
    """Test the various conditions that will cause the not_require_serialization
    function to return True.
    """
    if use_schema:
        assert not_require_serialization(fake_data_schema, test_input) is True
    else:
        assert not_require_serialization(None, test_input) is True


@pytest.mark.parametrize("test_input", [["Hello Word"], {"key": "This should pass"},])
def test_not_require_serialization_returns_false(test_input, fake_data_schema):
    """Test the various conditions that will cause the not_require_serialization
    function to return False.
    """
    assert not_require_serialization(fake_data_schema, test_input) is False


@patch("app.helpers.decorators.make_response")
def test_handle_serialization_argument_is_list(
    mock_make_response, fake_data_schema, fake_response
):
    """Test that when the input is a list that an attempt is made to serialize
    the data in the list.
    """

    mock_make_response.return_value = fake_response

    fake_results = fake_data_schema.dump({"name": "Ben"})
    flask_response = handle_serialization(
        ["Hello World"], fake_data_schema, HTTPStatus.OK
    )

    assert flask_response == fake_response
    assert flask_response.status_code == 200
    mock_make_response.assert_called_with(fake_results, HTTPStatus.OK)


@patch("app.helpers.decorators.serialize_model_or_models")
@patch("app.helpers.decorators.make_response")
def test_handle_serialization_argument_is_dict(
    mock_make_response, mock_serialize_model_or_models, fake_data_schema, fake_response
):
    """Test that when the input is a dictionary that the serialize_model_or_models
    function is called.
    """
    mock_make_response.return_value = fake_response
    arguments = {"username": "Fire124"}
    flask_response = handle_serialization(arguments, fake_data_schema, HTTPStatus.OK)

    assert flask_response == fake_response
    assert flask_response.status_code == 200
    mock_serialize_model_or_models.assert_called_with(arguments, fake_data_schema)



def test_serialize_model_or_models_with_models_in_dict(fake_data_schema):
    """Test to confirm that if any of keys of the passed in dictionary is 'model' or 'models',
    that the schema's dump method is called to serialize the that key-value pair.
    """

    # Test for just a singular model
    arguments = {"name": "John", "model": "Pretend a model object is here"}
    serialize_model_or_models(arguments, fake_data_schema)
    assert "User" in arguments
    assert "name" in arguments

    # Test for multiple models
    arguments = {"name": "John", "models": "Pretend a list of models are here"}
    serialize_model_or_models(arguments, fake_data_schema)
    assert "Users" in arguments
    assert "name" in arguments
