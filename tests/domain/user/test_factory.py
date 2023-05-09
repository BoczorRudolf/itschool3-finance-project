import unittest
from uuid import UUID

from domain.user.factory import UserFactory, InvalidUsername
from domain.user.user import User


class TestUserFactory(unittest.TestCase):
    def setUp(self):
        self.factory = UserFactory()

    def test_creates_user_with_valid_username_length(self):
        username = "between-6-and-20"

        actual_user = self.factory.make_new(username)

        self.assertEqual(username, actual_user.username)
        self.assertIsInstance(actual_user, User)

    def test_raises_exception_if_username_is_below_minimum_length(self):
        username = "below"

        with self.assertRaises(InvalidUsername) as context:
            self.factory.make_new(username)

        self.assertEqual(
            "Username should have at least 6 characters",
            str(context.exception)
        )

    def test_raises_exception_if_username_is_above_maximum_length(self):
        username = "a" * 21

        with self.assertRaises(InvalidUsername) as context:
            self.factory.make_new(username)

        self.assertEqual(
            "Username should have a maximum of 20 characters",
            str(context.exception)
        )

    def test_creates_user_with_valid_username_characters(self):
        username = "piu-bum623"

        actual_user = self.factory.make_new(username)

        self.assertEqual(username, actual_user.username)

    def test_raises_exception_if_username_contains_invalid_characters(self):
        username = "$#%@!m@1"

        with self.assertRaises(InvalidUsername) as context:
            self.factory.make_new(username)

        self.assertEqual(
            "Username should contain only alpha-numeric characters or '-'.",
            str(context.exception)
        )

    def test_make_user_from_persistence_info(self):
        uuid_str = "425181e7-82d7-4436-ac21-91c76b9a2157"
        username = "random-1"
        info = (uuid_str, username)

        user = self.factory.make_from_persistance(info)

        self.assertIsInstance(user, User)
        self.assertEqual(user.id, UUID(hex=uuid_str))
        self.assertEqual(user.username, username)


if __name__ == "__main__":
    unittest.main()

