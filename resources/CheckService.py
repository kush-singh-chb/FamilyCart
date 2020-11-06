import json
import os
import re

import requests
from flask_jwt_extended import (create_access_token, jwt_refresh_token_required,
                                get_jwt_identity)
from flask_restful import Resource

import validation
from validation import check_service_validate


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
