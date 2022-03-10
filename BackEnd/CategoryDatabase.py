"""
This class is to be used to access and modify the category DynamoDB database.
"""
import boto3
from boto3.dynamodb.conditions import Key


class CategoryDatabase:
    """ Class CategoryDatabase """

    def __init__(self):
        """ Initialize the connection to our category table """
        self.database = boto3.resource(
            'dynamodb',
            aws_access_key_id='AKIARGBHMBSJ3FAIIXLM',
            aws_secret_access_key='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',
            region_name='us-east-1')
        self.category_table = self.database.Table('CategoryTable')

    def create_category(self, user_name, category_name, category_desc):
        """ Method to create a new category for a user """
        response = self.category_table.put_item(
            Item={'userName': user_name,
                  'categoryName': category_name,
                  'description': category_desc})
        return response

    def update_category_desc(self, user_name, category_name, new_category_desc):
        """ Method to update an existing category for a user """
        response = self.category_table.update_item(
            Key={'userName': user_name,
                 'categoryName': category_name},
            UpdateExpression="set description = :desc",
            ExpressionAttributeValues={
                ':desc': new_category_desc},
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
