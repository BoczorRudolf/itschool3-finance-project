import unittest
import uuid
from domain.user.factory import UserFactory, InvalidUsername, InvalidPersistenceInfo
from domain.user.user import User


class UserFactoryTestCase(unittest.TestCase):
    def setUp(self):
        self.factory = UserFactory()

    def test_creates_user_with_valid_username(self):
        username = "between-6-and-20"
        actual_user = self.factory.make_new(username)
        self.assertEqual(username, actual_user.username)
        self.assertIsInstance(actual_user, User)

    def test_raises_exception_if_username_is_below_6_chars(self):
        username = "below"
        with self.assertRaises(InvalidUsername) as context:
            self.factory.make_new(username)
        self.assertEqual(
            "Username should have more than 6 characters", str(context.exception)
        )

    def test_raises_exception_if_username_is_above_20_chars(self):
        username = "aaaaaaaaaadddddddddddddwwwwwwwwww"
        with self.assertRaises(InvalidUsername) as context:
            self.factory.make_new(username)
        self.assertEqual(
            "The username should have a maximum of 20 characters", str(context.exception)
        )

    def test_creates_user_with_valid_chars_in_username(self):
        username = "Marduk-666"
        actual_user = self.factory.make_new(username)
        self.assertEqual(username, actual_user.username)

    def test_raises_exception_if_username_has_invalid_chars(self):
        username = "Marduk*77"
        with self.assertRaises(InvalidUsername) as context:
            self.factory.make_new(username)
        self.assertEqual(
            "The username must consist solely of alphanumeric characters or the hyphen (-) symbol.",
            str(context.exception),
        )

    def test_make_from_persistence_with_valid_info(self):
        valid_uuid = str(uuid.uuid4())
        valid_username = "mayhem_all"
        valid_info = (valid_uuid, valid_username)
        result = self.factory.make_from_persistence(valid_info)
        self.assertIsInstance(result, User)
        self.assertEqual(str(result.id), valid_uuid)
        self.assertEqual(result.username, valid_username)

    def test_make_from_persistence_with_invalid_info(self):
        invalid_uuid = "invalid-uuid"
        invalid_username = "user%name"
        invalid_info = (invalid_uuid, invalid_username)
        with self.assertRaises(InvalidPersistenceInfo) as context:
            self.factory.make_from_persistence(invalid_info)
        self.assertEqual(str(context.exception), "Invalid UUID: {}".format(invalid_uuid))


if __name__ == "__main__":
    unittest.main()
