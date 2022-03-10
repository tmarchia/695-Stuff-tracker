"""
This class is to be used to access and modify the item DynamoDB database.
"""
import boto3
from boto3.dynamodb.conditions import Key, Attr


class ItemDatabase:
    """ Class ItemDatabase """

    def __init__(self):
        """ Initialize the connection to our item table """
        self.database = boto3.resource(
            'dynamodb',
            aws_access_key_id='AKIARGBHMBSJ3FAIIXLM',
            aws_secret_access_key='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',
            region_name='us-east-1')
        self.item_table = self.database.Table('ItemTable')

    def add_item(self, user_name, item_name, item_desc, category):
        """ Method to create a new item for a user """
        response = self.item_table.put_item(
            Item={'userName': user_name,
                  'itemName': item_name,
                  'description': item_desc,
                  'category': category})

        return response

    def update_item(self, user_name, item_name, new_item_desc, new_category):
        """ Method to update an existing item's information for a user """
        response = self.item_table.update_item(
            Key={'userName': user_name,
                 'itemName': item_name},
            UpdateExpression="set description= :desc, category= :cat",
            ExpressionAttributeValues={
                ':desc': new_item_desc,
                ':cat': new_category})

        return response

    def delete_item(self, user_name, item_name):
        """ Method to delete an existing item for a user """
        response = self.item_table.delete_item(
            Key={'userName': user_name,
                 'itemName': item_name})
        return response

    def get_items_by_category(self, user_name, category):
        """ Method to get all items for a particular category """
        response = self.item_table.query(
            KeyConditionExpression=Key('userName').eq(user_name),
            FilterExpression=Attr('category').eq(category))

        return response['Items']
