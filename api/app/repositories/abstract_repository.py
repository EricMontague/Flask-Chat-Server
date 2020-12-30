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
    def update_user_image(self, user, image_data):
        pass

    @abstractmethod
    def remove_user(self, user_id):
        pass

    @abstractmethod
    def get_users(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_user_communities(self, user_id, *args, **kwargs):
        pass

    @abstractmethod
    def get_community(self, community_id):
        pass

    @abstractmethod
    def add_community(self, community, founder_id):
        pass

    @abstractmethod
    def update_community(self, community, attributes_to_update, *args, **kwargs):
        pass

    @abstractmethod
    def update_community_image(self, community, image_data):
        pass

    @abstractmethod
    def remove_community(self, community):
        pass

    @abstractmethod
    def get_communities(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_communities_by_topic(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_communities_by_location(self, *args, **kwargs):
        pass

    @abstractmethod
    def add_community_member(self, community_id, user_id):
        pass

    @abstractmethod
    def remove_community_member(self, community_id, user_id):
        pass

    @abstractmethod
    def get_community_members(self, community_id, *args, **kwargs):
        pass

    @abstractmethod
    def get_user_notifications(self, user_id, *args, **kwargs):
        pass

    @abstractmethod
    def add_user_notification(self, notification):
        pass

    @abstractmethod
    def get_user_notification(self, user_id, notification_id):
        pass


class FileStorageRepository(ABC):
    """Abstract base class for all repositories that deal with
    storing files and BLOB data.
    """

    def get(self, file_id):
        pass

    def add(self, file_id, file):
        pass

    def remove(self, file_id):
        pass

    
    