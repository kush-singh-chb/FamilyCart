from flask_jwt_extended import (create_access_token, create_refresh_token)
from flask_restful import Resource

import validation
from models.UserModel import UserModel
from validation import login_validate


class UserLogin(Resource):
    def post(self):
        data = login_validate().parse_args()
        if not validation.validate_eir(data['eircode']):
            return {'message': 'Invalid eircode'}, 422
        current_user = UserModel.find_by_username(data['email'])

        if not current_user:
            return {'message': 'User {} doesn\'t exist'.format(data['email'])}

        if UserModel.verify_hash(data['password'], current_user.password):
            access_token = create_access_token(identity=data['email'])
            refresh_token = create_refresh_token(identity=data['email'])
            return {
                'message': 'Logged in as {}'.format(current_user.username[0]),
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        else:
            return {'message': 'Wrong credentials'}
