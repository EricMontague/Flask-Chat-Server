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
    def get_user_by_email(self, email):
        pass

    @abstractmethod
    def get_user_by_username(self, username):
        pass

    @abstractmethod
    def add_user(self, user):
        pass

    @abstractmethod
    def get_user_token(self, user_id):
        pass

    @abstractmethod
    def get_user_tokens(self, user_id):
        pass

    @abstractmethod
    def get_token(self, user_id, token_type):
        pass

    @abstractmethod
    def add_token(self, token):
        pass

    @abstractmethod
    def remove_token(self, token):
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
    def get_community_by_name(self, community_name):
        pass

    @abstractmethod
    def get_community_membership(self, community_id, user_id):
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

    @abstractmethod
    def add_private_chat(self, private_chat, primary_user_id, secondary_user_id):
        pass

    @abstractmethod
    def get_user_private_chats(self, user_id):
        pass

    @abstractmethod
    def get_private_chat_messages(self, private_chat_id):
        pass

    @abstractmethod
    def get_group_chat_message(self, message_id):
        pass

    @abstractmethod
    def add_group_chat_message(self, message):
        pass

    @abstractmethod
    def remove_group_chat_message(self, message):
        pass

    @abstractmethod
    def get_private_chat_message(self, message_id):
        pass

    @abstractmethod
    def add_private_chat_message(self, message):
        pass

    @abstractmethod
    def remove_private_chat_message(self, message):
        pass

    @abstractmethod
    def add_group_chat(self, group_chat):
        pass

    @abstractmethod
    def update_group_chat(self, group_chat, updated_group_chat_data):
        pass

    @abstractmethod
    def remove_group_chat_member(self, group_chat_id, user_id):
        pass

    @abstractmethod
    def get_group_chat_messages(self, group_chat_id, *args, **kwargs):
        pass
    
    @abstractmethod
    def get_group_chat_member(self, group_chat_id, user_id):
        pass

    @abstractmethod
    def get_group_chat_members(self, group_chat_id, *args, **kwargs):
        pass

    @abstractmethod
    def get_community_group_chats(self, community_id, *args, **kwargs):
        pass


class FileStorageRepository(ABC):
    """Abstract base class for all repositories that deal with
    storing files and BLOB data.
    """

    @abstractmethod
    def get(self, file_id):
        pass

    @abstractmethod
    def add(self, file_id, file):
        pass

    @abstractmethod
    def remove(self, file_id):
        pass

