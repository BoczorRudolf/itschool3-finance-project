import os
import unittest

from domain.exceptions import DuplicateUser
from domain.user.factory import UserFactory
from domain.user.repo import UserRepo
from persistence.asset_file import AssetFilePersistence
from persistence.user_file import UserPersistenceFile

class UserRepoTestCase(unittest.TestCase):
    # asset_persistence = None
    # persistence = None

    assets_file = None
    asset_persistence = None
    persistence = None
    users_file = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.users_file = "test_users.json"
        cls.assets_file = "test_assets.json"
        cls.persistence = UserPersistenceFile(cls.users_file)
        cls.asset_persistence = AssetFilePersistence(cls.assets_file)
        cls.repo = UserRepo(cls.persistence, cls.asset_persistence)

    def test_it_adds_a_user(self):
        expected_username = "unique-username"  # change to a unique username
        new_user = UserFactory().make_new(expected_username)

        try:
            self.repo.add(new_user)
        except DuplicateUser:
            self.fail("Could not add user")

        actual_users = self.repo.get_all()

        self.assertEqual(1, len(actual_users))
        self.assertEqual(expected_username, actual_users[0].username)

    def test_it_deletes_a_user(self):
        expected_username = "given-username7"
        new_user = UserFactory().make_new(expected_username)

        self.repo.add(new_user)

        self.repo.delete_by_id(str(new_user.id))

        users_list = [u.id for u in self.repo.get_all()]
        self.assertNotIn(str(new_user.id), users_list)


    def test_it_edits_a_user(self):
        # Arrange
        old_username = "given-username3"
        new_username = "given-username"
        new_user = UserFactory().make_new(old_username)
        self.repo.add(new_user)

        # Act
        self.repo.edit(str(new_user.id), new_username)
        actual_user = self.repo.get_by_id(str(new_user.id))
        all_usernames = [u.username for u in self.repo.get_all()]

        # Assert
        self.assertEqual(new_username, actual_user.username)
        self.assertIn(new_username, all_usernames)
        self.assertNotIn(old_username, all_usernames)

    def test_it_gets_a_user_by_id(self):
        # Arrange
        expected_username = "given-username"
        new_user = UserFactory().make_new(expected_username)
        self.repo.add(new_user)

        # Act
        actual_user = self.repo.get_by_id(str(new_user.id))

        # Assert
        self.assertEqual(expected_username, actual_user.username)

    @classmethod
    def tearDownClass(cls) -> None:
        os.remove("test_users.json")




if __name__ == "__main__":
    unittest.main()