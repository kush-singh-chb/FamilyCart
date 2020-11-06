import os

import boto3

db = boto3.resource(service_name='dynamodb', region_name='eu-west-1',
                    aws_access_key_id=os.environ.get("aws_access_key_id"),
                    aws_secret_access_key=os.environ.get("aws_secret_access_key"))


class UserCart:
    __tablename__ = 'userCart'
    id: str
    products = []
    total = 0.0
