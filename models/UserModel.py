import os
from uuid import uuid4

import boto3
from passlib.hash import pbkdf2_sha256 as sha256

db = boto3.resource(service_name='dynamodb', region_name='eu-west-1',
                    aws_access_key_id=os.environ.get("aws_access_key_id"),
                    aws_secret_access_key=os.environ.get("aws_secret_access_key"))


class UserModel:
    __tablename__ = 'users'
    id = uuid4()
    username: str
    email: str
    firstname: str
    lastname: str
    password: str
    eir_code: str
    orders = []
    usercart: str

    def save_to_db(self):
        res = db.Table(UserModel.__tablename__).put_item(
            Item={
                'id': self.id,
                'email': self.username[0],
                'first_name': self.firstname,
                'password': self.password,
                'last_name': self.lastname,
                'eir_code': self.eir_code,
                'orders': self.orders,
                'usercart': self.usercart
            }
        )
        print(res)

    @classmethod
    def find_by_username(cls, username):
        response = db.Table(UserModel.__tablename__).get_item(Key={
            'username': username
        })
        user = UserModel()
        user.username = response['Item']['username'],
        user.password = response['Item']['password'],
        user.firstname = response['Item']['first_name'],
        return user

    @staticmethod
    def create_user_table():
        try:
            table = db.create_table(
                TableName=UserModel.__tablename__,
                KeySchema=[
                    {
                        'AttributeName': 'email',
                        'KeyType': 'HASH'
                    }
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'email',
                        'AttributeType': 'S'
                    }
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                }
            )

            # Wait until the table exists.
            table.meta.client.get_waiter('table_exists').wait(TableName='users')
        except Exception as e:
            print(e)
            pass

    @classmethod
    def check_by_username(cls, email):
        response = db.Table(UserModel.__tablename__).get_item(Key={
            'email': email,
        })
        return "Item" in response

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash[0])
