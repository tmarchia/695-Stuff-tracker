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
        """ Tests adding item """
        mock_table = Mock()
        mock_table.put_item.return_value = True
        mock_dynamo.return_value.Table.return_value = mock_table

        item_db = ItemDatabase.ItemDatabase()
        ret_val = item_db.add_item(
            'testUser', 'shirt', '', 'closet', 'dresser', '01-01-2022', 'pink,summer')
        expected_result = True
        self.assertEqual(expected_result, ret_val)

    @patch('boto3.resource')
    def test_update_item_loc(self, mock_dynamo):
        """ Tests updating item """
        mock_table = Mock()
        mock_table.put_item.return_value = True
        mock_table.update_item.return_value = True
        mock_dynamo.return_value.Table.return_value = mock_table

        item_db = ItemDatabase.ItemDatabase()
        ret_val = item_db.add_item(
            'testUser', 'shirt', '', 'closet', 'dresser', '01-01-2022', 'pink,summer')
        ret_val = item_db.update_item('testUser', 'shirt', 'closet', 'rack')

        expected_result = True
        self.assertEqual(expected_result, ret_val)

    @patch('boto3.resource')
    def test_delete_item(self, mock_dynamo):
        """ Tests deleting item """
        mock_table = Mock()
        mock_table.put_item.return_value = True
        mock_table.delete_item.return_value = True
        mock_dynamo.return_value.Table.return_value = mock_table

        item_db = ItemDatabase.ItemDatabase()
        ret_val = item_db.add_item(
            'testUser', 'shirt', '', 'closet', 'dresser', '01-01-2022', 'pink,summer')
        item_db.delete_item('testUser', 'shirt')

        expected_result = True
        self.assertEqual(expected_result, ret_val)


if __name__ == "__main__":
    unittest.main(exit=False, verbosity=2)
