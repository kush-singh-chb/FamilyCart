import os
from uuid import uuid4

import boto3

db = boto3.resource(service_name='dynamodb', region_name='eu-west-1',
                    aws_access_key_id=os.environ.get("aws_access_key_id"),
                    aws_secret_access_key=os.environ.get("aws_secret_access_key"))


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
