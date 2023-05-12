import unittest
from domain.user.factory import UserFactory, InvalidUsername
from domain.user.user import User


class UserFactoryTestCase(unittest.TestCase):
    def setUp(self):
        self.factory = UserFactory()

    def test_it_creates_user_if_the_username_is_between_6_and_20_chars(self):
        username = "between-6-and-20-"
        actual_user = self.factory.make_new(username)
        self.assertEqual(username, actual_user.username)
        self.assertIsInstance(actual_user, User)

    def test_it_raises_exception_if_the_username_is_below_6(self):
        username = "below"
        with self.assertRaises(InvalidUsername) as context:
            self.factory.make_new(username)
        self.assertEqual(
            "Username should have at least 6 chars", str(context.exception)
        )

    def test_it_raises_exception_if_the_username_is_above_20_chars(self):
        username = "u" * 21
        with self.assertRaises(InvalidUsername) as context:
            self.factory.make_new(username)
        self.assertEqual(
            "Username should have a maximum of 20 chars!",
            str(context.exception).strip(),
        )

    def test_it_creates_a_user_if_the_username_has_valid_chars(self):
        username = "fire1-23"
        actual_user = self.factory.make_new(username)
        self.assertEqual(username, actual_user.username)
        self.assertIsInstance(actual_user, User)

    def test_it_raises_exception_if_the_username_has_invalid_chars(self):
        username = "333@mayhem"
        with self.assertRaises(InvalidUsername) as context:
            self.factory.make_new(username)
        self.assertEqual(
            "Username should have only letters and numbers as characters or '-'.",
            str(context.exception).strip(),
        )

    def test_make_from_persistence(self):
        uuid_ = "70f5b392-a479-49bb-a372-c26039261613"
        username = "string-6"
        info = (uuid_, username)
        user = self.factory.make_from_persistence(info)
        self.assertIsInstance(user, User)


if __name__ == "__main__":
    unittest.main()
