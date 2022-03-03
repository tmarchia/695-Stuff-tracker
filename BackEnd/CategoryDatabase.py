"""
This class is to be used to access and modify the category DynamoDB database.
"""
import boto3


class CategoryDatabase:
    """ Class CategoryDatabase """

    def __init__(self, database_url="http://localhost:8000"):
        """ Initialize the connection to our category table """
        self.database = boto3.resource(
            'dynamodb', endpoint_url=database_url, region_name='us-east-1')
        self.category_table = self.database.Table('CategoryTable')

    def create_category(self, user_name, category_name, category_desc):
        """ Method to create a new category for a user """
        response = self.category_table.put_item(
            Item={'UserName': user_name,
                  'Category': category_name,
                  'Description': category_desc})

        return response

    def update_category_desc(self, user_name, category_name, new_category_desc):
        """ Method to update an existing category for a user """
        response = self.category_table.update_item(
            Key={'UserName': user_name,
                 'Category': category_name},
            UpdateExpression={"SET Description= :desc"},
            ExpressionAttributeValues={
                ':desc': new_category_desc})

        return response

    def get_categories(self, user_name):
        """ Method to return list of all categories for a user """
        response = self.query(
            KeyConditionExpression=Key('UserName').eq(user_name))

        return response['Items']
