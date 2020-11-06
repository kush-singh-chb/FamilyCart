import re

from flask_jwt_extended import (create_access_token, create_refresh_token)
from flask_restful import Resource

import validation
from models.UserModel import UserModel
from validation import register_validate


class UserRegistration(Resource):
    def post(self):
        data = register_validate().parse_args()
        if not validation.validate_email(email=data['email']):
            return {'message': 'Invalid Email'}, 422
        if not re.match('^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$', data['password']):
            return {'message': 'Stronger Password required'}, 422
        if UserModel.check_by_username(data['email']):
            return {'message': 'User {} already exists'.format(data['email'])}, 422
        else:
            new_user = UserModel()
            new_user.username = data['email'],
            new_user.firstname = data['first_name']
            new_user.password = UserModel.generate_hash(data['password'])
            try:
                new_user.save_to_db()
                access_token = create_access_token(identity=data['email'][0])
                refresh_token = create_refresh_token(identity=data['email'][0])
                return {
                    'message': 'User {} was created'.format(data['email']),
                    'access_token': access_token,
                    'refresh_token': refresh_token
                }
            except:
                return {'message': 'Something went wrong'}, 500
