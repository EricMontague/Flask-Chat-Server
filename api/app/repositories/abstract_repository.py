"""This module contains the abstract base classes for all repositories."""


from abc import ABC, abstractmethod


class AbstractDatabaseRepository(ABC):
    """Abstract base class for all repositories that interact
    with the databse layer.
    """

    @abstractmethod
    def get_user(self, user_id):
        pass

    @abstractmethod
    def add_user(self, user):
        pass

    @abstractmethod
    def update_user(self, user, attributes_to_update, *args, **kwargs):
        pass

    @abstractmethod
    def remove_user(self, user_id):
        pass

    @abstractmethod
    def get_users(self, *args, **kwargs):
        pass
