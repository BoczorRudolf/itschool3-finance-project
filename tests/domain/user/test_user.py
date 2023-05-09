import unittest
import uuid
from domain.user.user import User


class UserMyTasteCase(unittest.TestCase):
    def test_user_sets_the_right_username(self):
        # set up
        username = "random-generated"
        id_ = uuid.uuid4()
        user = User(id_, username)
        # execution
        actual_username = user.username
        # assertion
        self.assertEqual(username, actual_username)

    def test_it_sets_empty_list_if_we_do_not_specify_stock(self):
        id_ = uuid.uuid4()
        username = "random-username"
        user = User(id_, username)

        actual_stocks = user.stocks

        self.assertEqual([], actual_stocks)

    def test_it_sets_the_stocks_we_give(self):
        id_ = uuid.uuid4()
        username = "random-name"
        stock_list = ["first", "second", "third"]

        user = User(id_, username, stock_list)

        actual = user.stocks

        self.assertEqual(stock_list, actual)


if __name__ == "__main__":
    unittest.main()
