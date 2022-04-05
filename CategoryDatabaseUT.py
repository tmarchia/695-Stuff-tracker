"""
This class unit tests our category database accessor class
"""


import unittest
from unittest.mock import Mock, patch
from BackEnd import CategoryDatabase


class CategoryDatabaseTest(unittest.TestCase):
    """ Class test for category database """

    @patch('boto3.resource')
    def test_create_category(self, mock_dynamo):
        mock_table = Mock()
        mock_table.put_item.return_value = True
        mock_dynamo.return_value.Table.return_value = mock_table

        categoryDb = CategoryDatabase.CategoryDatabase()
        retVal = categoryDb.create_category('testUser', 'bedroom', 'dresser')

        expected_result = True
        self.assertEqual(expected_result, retVal)

    @patch('boto3.resource')
    def test_update_category_loc(self, mock_dynamo):
        mock_table = Mock()
        mock_table.put_item.return_value = True
        mock_table.update_item.return_value = True
        mock_dynamo.return_value.Table.return_value = mock_table

        categoryDb = CategoryDatabase.CategoryDatabase()
        retVal = categoryDb.create_category('testUser', 'bedroom', 'dresser')
        retVal = categoryDb.update_category_loc('testUser', 'bedroom', 'closet')

        expected_result = True
        self.assertEqual(expected_result, retVal)

    @patch('boto3.resource')
    def test_delete_category(self, mock_dynamo):
        mock_table = Mock()
        mock_table.put_item.return_value = True
        mock_table.delete_item.return_value = True
        mock_dynamo.return_value.Table.return_value = mock_table

        categoryDb = CategoryDatabase.CategoryDatabase()
        retVal = categoryDb.create_category('testUser', 'bedroom', 'dresser')
        categoryDb.delete_category('testUser', 'dresser')

        expected_result = True
        self.assertEqual(expected_result, retVal)


if __name__ == "__main__":
    unittest.main(exit=False, verbosity=2)
