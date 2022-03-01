"""
This class is to be used to access and modify the item DynamoDB database.
"""
import boto3


class ItemDatabase:
    """ Class ItemDatabase """

    def __init__(self, databaseUrl="http://localhost:8000"):
        """ Initialize the connection to our item table """
        self.database = boto3.resource(
            'dynamodb', endpoint_url=databaseUrl, region_name='us-east-1')
        self.category_table = self.database.Table('Items')

    def add_item(self, userId, category_name, item_name, item_description):
        """ TODO """
        return
