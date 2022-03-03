"""
This class unit tests our category database accessor class
"""


from BackEnd import CategoryDatabase
import unittest
from moto import mock_dynamodb2
import store


class CategoryDatabaseTest(unittest.TestCase):
    """ Class test for category database """
    """ WORK IN PROGRESS """

    @mock_dynamodb2
    def test_databaseInit(self):
        """ Tests that tests initializing the database connection """
        database = CategoryDatabase.CategoryDatabase()
        ret = database.create_category(
            "12345", "Closet Items", "This category contains all items found in my closet.")

        self.assertEqual(ret, True)


if __name__ == "__main__":
    unittest.main(exit=False, verbosity=2)
