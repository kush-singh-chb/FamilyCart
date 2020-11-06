import os
from datetime import datetime
from uuid import uuid4

import boto3

db = boto3.resource(service_name='dynamodb', region_name='eu-west-1',
                    aws_access_key_id=os.environ.get("aws_access_key_id"),
                    aws_secret_access_key=os.environ.get("aws_secret_access_key"))


class CategoryModel:
    __tablename__ = "ethnicCategory"
    id = str(uuid4())
    name: str
    stores = []
    createdOn: str
    updatedOn = datetime.now().isoformat()

    def save_to_db(self):
        db.Table(CategoryModel.__tablename__).put_item(Item={
            'id': self.id,
            'name': self.name,
            'stores': self.stores,
            'createdOn': self.createdOn,
            'updatedOn': self.updatedOn
        })

    @staticmethod
    def get_ethnic_category_by_id(_id):
        res = db.Table(CategoryModel.__tablename__).get_item(Key={
            'id': _id
        })
        return res['Item']

    @staticmethod
    def get_categories():
        res = db.Table(CategoryModel.__tablename__).scan()
        print(res)
        return res['Items']
