"""
This class unit tests our Item database accessor class
"""


import unittest
from unittest.mock import Mock, patch
from BackEnd import ItemDatabase


class ItemDatabaseTest(unittest.TestCase):
    """ Class test for Item database """

    @patch('boto3.resource')
    def test_add_item(self, mock_dynamo):
        mock_table = Mock()
        mock_table.put_item.return_value = True
        mock_dynamo.return_value.Table.return_value = mock_table

        ItemDb = ItemDatabase.ItemDatabase()
        retVal = ItemDb.add_item(
            'testUser', 'shirt', 'closet', 'dresser', '01-01-2022', 'pink,summer')
        expected_result = True
        self.assertEqual(expected_result, retVal)

    @patch('boto3.resource')
    def test_update_item_loc(self, mock_dynamo):
        mock_table = Mock()
        mock_table.put_item.return_value = True
        mock_table.update_item.return_value = True
        mock_dynamo.return_value.Table.return_value = mock_table

        ItemDb = ItemDatabase.ItemDatabase()
        retVal = ItemDb.add_item(
            'testUser', 'shirt', 'closet', 'dresser', '01-01-2022', 'pink,summer')
        retVal = ItemDb.update_item('testUser', 'shirt', 'closet', 'rack')

        expected_result = True
        self.assertEqual(expected_result, retVal)

    @patch('boto3.resource')
    def test_delete_item(self, mock_dynamo):
        mock_table = Mock()
        mock_table.put_item.return_value = True
        mock_table.delete_item.return_value = True
        mock_dynamo.return_value.Table.return_value = mock_table

        ItemDb = ItemDatabase.ItemDatabase()
        retVal = ItemDb.add_item(
            'testUser', 'shirt', 'closet', 'dresser', '01-01-2022', 'pink,summer')
        ItemDb.delete_item('testUser', 'shirt')

        expected_result = True
        self.assertEqual(expected_result, retVal)


if __name__ == "__main__":
    unittest.main(exit=False, verbosity=2)
