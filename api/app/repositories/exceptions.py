"""This module contains exceptions for the repository layer."""


class DatabaseException(Exception):
    """Base class for all exceptions raised in a repository
    that inherits from AbstractDatabaseRepository.
    """


class UniqueConstraintException(DatabaseException):
    """Raised when a unique constraint is violated at
    the database layer.
    """
    