"""
This class is to be used to access and modify the item DynamoDB database.
"""
import os
import boto3
from boto3.dynamodb.conditions import Key, Attr


class ItemDatabase:
    """ Class ItemDatabase """

    def __init__(self):
        """ Initialize the connection to our item table """
        access_key_id = ''
        secret_access_key = ''
        key_file_path = '/home/ec2-user/config/FixerKeys.txt'
        if(os.path.exists(key_file_path)):
            with open(key_file_path) as key_file:
                lines = key_file.readlines()
                access_key_id = lines[0].split(':')[1].strip()
                secret_access_key = lines[1].split(':')[1].strip()

        self.database = boto3.resource(
            'dynamodb',
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key,
            region_name='us-east-1')
        self.item_table = self.database.Table('ItemTable')

    def add_item(self, user_name, item_name, category, location, purchase_date, tags):
        """ Method to create a new item for a user """
        tags_list = tags.split(',')
        response = self.item_table.put_item(
            Item={'userName': user_name,
                  'itemName': item_name,
                  'category': category,
                  'location': location,
                  'purchase_date': purchase_date,
                  'tags': tags_list})

        return response

    def update_item(self, user_name, item_name, new_category, new_location):
        """ Method to update an existing item's information for a user """
        response = self.item_table.update_item(
            Key={'userName': user_name,
                 'itemName': item_name},
            UpdateExpression="set category= :cat, location= :loc",
            ExpressionAttributeValues={
                ':cat': new_category,
                ':loc': new_location})

        return response

    def delete_item(self, user_name, item_name):
        """ Method to delete an existing item for a user """
        response = self.item_table.delete_item(
            Key={'userName': user_name,
                 'itemName': item_name})
        return response

    def get_all_items(self, user_name):
        """ Method to get all items for a particular category """
        response = self.item_table.query(
            KeyConditionExpression=Key('userName').eq(user_name))

        return response['Items']

    def get_items_by_category(self, user_name, category):
        """ Method to get all items for a particular category """
        response = self.item_table.query(
            KeyConditionExpression=Key('userName').eq(user_name),
            FilterExpression=Attr('category').eq(category))

        return response['Items']

    def get_item_by_name(self, user_name, item_name):
        """ Method to get all items for a particular category """
        response = self.item_table.query(
            KeyConditionExpression=Key('userName').eq(user_name),
            FilterExpression=Attr('itemName').eq(item_name))

        return response['Items']
