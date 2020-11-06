import os
from uuid import uuid4

import boto3

db = boto3.resource(service_name='dynamodb', region_name='eu-west-1',
                    aws_access_key_id=os.environ.get("aws_access_key_id"),
                    aws_secret_access_key=os.environ.get("aws_secret_access_key"))


class Store:
    id: str = uuid4()
    name: str
    eircode: str
