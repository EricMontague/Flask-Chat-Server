"""This file contains a class that uses the faker package for
inserted fake data into the database.
"""


from faker import Faker
from app.clients import dynamodb_client
from app.dynamodb import UserMapper, UsernameMapper, UserEmailMapper
from app.models.user_factory import UserFactory
from app.models import UserEmail, Username


user_mapper = UserMapper()
username_mapper = UsernameMapper()
user_email_mapper = UserEmailMapper()


class FakeDataGenerator:
    """Class to generate fake data for the application."""

    def __init__(self, num_users=25):
        self._faker = Faker()
        self.num_users = num_users

    def add_users(self):
        """Add fake user data to the database."""

        remaining_users = self.num_users
        while remaining_users > 0:
            requests = []
            user_data = self._generate_fake_user_data()
            user = UserFactory.create_user(user_data)
            user_email = UserEmail(user.id, user.email)
            username = Username(user.id, user.username)
            requests.append(
                (
                    "PutRequest", 
                    user_mapper.serialize_from_model(
                        user, 
                        additional_attributes={"USERS_GSI_SK": user.username}
                    )
                )
            )
            requests.append(("PutRequest", user_email_mapper.serialize_from_model(user_email)))
            requests.append(("PutRequest", username_mapper.serialize_from_model(username)))
            response = dynamodb_client.batch_write_items(requests)
            remaining_users -= 1

    def add_notifications(self):
        """Add fake notification data to the database."""
        pass

    def add_chat_requests(self):
        """Add fake chat request data to the database."""
        pass

    def add_communities(self):
        """Add fake community data to the database."""
        pass

    def add_group_chats(self):
        """Add fake group chat data to the database."""
        pass

    def add_private_chats(self):
        """Add fake private chat data to the database."""
        pass

    def _generate_fake_user_data(self):
        """Return fake user data as a dictionary."""
        name = self._faker.name()
        fake_user_data = {
            "name": name,
            "username": name + "123",
            "email": self._faker.email(),
            "password": "password",
            "location": {
                "city": self._faker.city(),
                "state": self._faker.state(),
                "country": "United States"
            }
        }
        return fake_user_data