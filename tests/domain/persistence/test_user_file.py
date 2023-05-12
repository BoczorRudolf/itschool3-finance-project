import os
import unittest

from domain.user.factory import UserFactory
from persistence.user_file import UserPersistenceFile


class TestUserPersistenceFile(unittest.TestCase):
    def setUp(self):
        self.users_file = "test_users.json"
        self.persistence_file = UserPersistenceFile(self.users_file)

    def tearDown(self):
        os.remove(self.users_file)

    def test_add_user(self):
        expected_username = "given-username"
        new_user = UserFactory().make_new(expected_username)
        self.persistence_file.add(new_user)

        actual_users = self.persistence_file.get_all()
        self.assertEqual(1, len(actual_users))
        self.assertEqual(expected_username, actual_users[0].username)

    def test_read_users_from_file(self):
        a_username = "given-username"
        new_user = UserFactory().make_new(a_username)
        self.persistence_file.add(new_user)

        actual_users = self.persistence_file.get_all()
        self.assertIsNotNone(actual_users)
        self.assertIn(a_username, [u.username for u in actual_users])

    def test_delete_user_from_file(self):
        a_username = "given-username"
        new_user = UserFactory().make_new(a_username)
        self.persistence_file.add(new_user)

        self.persistence_file.delete_by_id(str(new_user.id))
        all_ids = [str(u.id) for u in self.persistence_file.get_all()]
        self.assertNotIn(str(new_user.id), all_ids)

    def test_edit_username_to_file(self):
        new_user = UserFactory().make_new("username-before")
        self.persistence_file.add(new_user)

        self.persistence_file.edit(str(new_user.id), "new-username")
        all_usernames = [u.username for u in self.persistence_file.get_all()]
        self.assertIn("new-username", all_usernames)
