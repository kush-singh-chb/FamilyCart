import json
import os

from flask import render_template, make_response
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required,
                                get_jwt_identity, get_raw_jwt)
from validate_email import validate_email
from flask_restful import Resource
import re
import requests

import validation
from models import UserModel, RevokedTokenModel
from validation import register_validate, login_validate, check_service_validate


class UserRegistration(Resource):
    def post(self):
        data = register_validate().parse_args()
        if not validate_email(email=data['email'], verify=True, check_mx=True,
                              smtp_timeout=10,
                              debug=False):
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


class UserLogin(Resource):
    def post(self):
        data = login_validate().parse_args()
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


class UserLogoutAccess(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel()
            revoked_token.jti = jti
            revoked_token.add()
            return {'message': 'Access token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500


class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel()
            revoked_token.jti = jti
            revoked_token.add()
            return {'message': 'Refresh token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return {'access_token': access_token}


class CheckService(Resource):
    def post(self):
        data = check_service_validate().parse_args()
        if not re.match(validation.eir_code_pattern, data['eircode']):
            return {'message': 'Invalid eircode'}, 422
        url = "https://graphhopper.com/api/1/route?"
        header = {
            "Content-Type": "application/json"
        }
        params = {
            "key": os.environ['grasshopper'],
        }
        data = {"points": [
            [
                -6.2782037,
                53.3407837
            ],
            [
                -6.2656517,
                53.3217209
            ]
        ],
            "vehicle": "car",
            "locale": "en",
            "elevation": False,
            "optimize": "false",
            "calc_points": True,
            "debug": False,
            "points_encoded": True,
            "ch.disable": True,
            "weighting": "fastest"
        }

        route_request = requests.post(url=url, params=params, data=json.dumps(data), headers=header)
        route_response = json.loads(route_request.text)
        if int(route_response['paths'][0]['distance']) / 1000.0 < 4.0:
            return {'message': 'Service available with in {} kms'.format(
                int(route_response['paths'][0]['distance']) / 1000.0)}, 201
        else:
            return {'message': 'Service unavailable'}, 201


class MainRoute(Resource):
    def get(self):
        return make_response(render_template('swagger-ui.html'))
