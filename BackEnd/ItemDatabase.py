"""
This class is to be used to access and modify the item DynamoDB database.
"""
import boto3


class ItemDatabase:
    """ Class ItemDatabase """

    def __init__(self, database_url="http://localhost:8000"):
        """ Initialize the connection to our item table """
        self.database = boto3.resource(
            'dynamodb', endpoint_url=database_url, region_name='us-east-1')
        self.item_table = self.database.Table('ItemTable')

    def add_item(self, user_name, item_name, item_desc, category):
        """ Method to create a new item for a user """
        response = self.item_table.put_item(
            Item={'UserName': user_name,
                  'ItemName': item_name,
                  'Description': item_desc,
                  'Category': category})

        return response

    def update_item(self, item_name, user_name, new_item_desc, new_category):
        """ Method to update an existing item's information for a user """
        response = self.item_table.update_item(
            Key={'UserName': user_name,
                 'ItemName': item_name},
            UpdateExpression={
                "SET Description= :desc, Category= :cat"},
            ExpressionAttributeValues={
                ':desc': new_item_desc,
                ':cat': new_category})

        return response

    def remove_item(self, user_name, item_name):
        """ Method to remove an existing item for a user """
        response = self.item_table.delete_item(
            Key={'UserName': user_name,
                 'ItemName': item_name})
        return response
