"""
This class is to be used to access and modify the category DynamoDB database.
"""
import os
import boto3
from boto3.dynamodb.conditions import Key


class CategoryDatabase:
    """ Class CategoryDatabase """

    def __init__(self):
        """ Initialize the connection to our category table """
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
        self.category_table = self.database.Table('CategoryTable')

    def create_category(self, user_name, category_name, location):
        """ Method to create a new category for a user """
        response = self.category_table.put_item(
            Item={'userName': user_name,
                  'categoryName': category_name,
                  'categoryLocation': location})
        return response

    def update_category_loc(self, user_name, category_name, new_location):
        """ Method to update an existing category for a user """
        response = self.category_table.update_item(
            Key={'userName': user_name,
                 'categoryName': category_name},
            UpdateExpression="set categoryLocation = :loc",
            ExpressionAttributeValues={
                ':loc': new_location},
            ReturnValues="UPDATED_NEW")

        return response

    def delete_category(self, user_name, category_name):
        """ Method to delete an existing category """
        response = self.category_table.delete_item(
            Key={'userName': user_name,
                 'categoryName': category_name})

    def get_categories(self, user_name):
        """ Method to return list of all categories for a user """
        response = self.category_table.query(
            KeyConditionExpression=Key('userName').eq(user_name))

        return response['Items']
