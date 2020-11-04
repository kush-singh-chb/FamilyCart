from uuid import uuid4

import boto3
from passlib.hash import pbkdf2_sha256 as sha256

db = boto3.resource('dynamodb')


class UserModel:
    __tablename__ = 'users'
    id = uuid4()
    username = None
    email = None
    firstname = None
    lastname = None
    password = None

    def save_to_db(self):
        res = db.Table(UserModel.__tablename__).put_item(
            Item={
                'email': self.username[0],
                'first_name': self.firstname,
                'password': self.password
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


class RevokedTokenModel:
    __tablename__ = 'revoked_tokens'
    id = uuid4()
    jti = None

    @staticmethod
    def create_revoke_table():
        try:
            table = db.create_table(
                TableName=RevokedTokenModel.__tablename__,
                KeySchema=[
                    {
                        'AttributeName': 'jwt',
                        'KeyType': 'HASH'
                    }
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'jwt',
                        'AttributeType': 'S'
                    }
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                }
            )

            # Wait until the table exists.
            table.meta.client.get_waiter('table_exists').wait(TableName=RevokedTokenModel.__tablename__)
        except Exception as e:
            print(e)
            pass

    def add(self):
        db.Table(RevokedTokenModel.__tablename__).put_item(Item={
            'jwt': self.jti,
            'id': self.id
        })

    @classmethod
    def is_jti_blacklisted(cls, jti):
        response = db.Table(RevokedTokenModel.__tablename__).get_item(Key={
            'jwt': jti,

        })
        return len(response) < 0
