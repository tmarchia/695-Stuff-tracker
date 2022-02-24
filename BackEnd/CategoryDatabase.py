"""
This class is to be used to access and modify the category DynamoDB database.
"""
import boto3


class CategoryDatabase:
    """ Class CategoryDatabase """

    def __init__(self, databaseUrl="http://localhost:8000"):
        """ Initialize the connection to our category table """
        self.database = boto3.resource(
            'dynamodb', endpoint_url=databaseUrl, region_name='us-west-2')
        self.category_table = self.database.Table('Categories')

    def create_category(self, userId, category_name, category_description):
        """ Method to create a new category for a user """
        response = self.category_table.put_item(
            Item={'category': category_name,
                  'description': category_description,
                  'user': userId})

        return response

    def get_categories(self, userId):
        """ Method to return list of all categories for a user """
        response = self.category_table(
            KeyConditionExpression=Key('user').eq(userId))

        return response['Items']
