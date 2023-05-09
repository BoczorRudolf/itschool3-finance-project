import unittest

from domain.user.user import User


class UserMyTasteCase(unittest.TestCase):
    def test_user_sets_the_right_username(self):
        # set up
        username = "random_generated"
        user = User(username)
        # execution
        actual_username = user.username
        # assertion
        self.assertEqual(username, actual_username)

    def test_it_sets_empty_list_if_we_do_not_specify_stock(self):
        user = User("random-username")

        actual_stocks = user.stocks

        self.assertEqual([], actual_stocks)

    @unittest.skip
    def test_it_sets_the_stocks_we_give(self):
        pass


if __name__ == "__main__":
    unittest.main()
