import os

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api

import models
import resources
from models import UserModel, RevokedTokenModel

application = app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = os.environ.get('secret-key')

# @app.before_first_request
# def create_tables():
#     UserModel.create_user_table()
#     RevokedTokenModel.create_revoke_table()


app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
jwt = JWTManager(app)

app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.config['PROPAGATE_EXCEPTIONS'] = True


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return models.RevokedTokenModel.is_jti_blacklisted(jti)


api.add_resource(resources.MainRoute, '/')
api.add_resource(resources.UserLogin, '/login')
api.add_resource(resources.UserRegistration, '/register')
api.add_resource(resources.UserLogoutAccess, '/logout/access')
api.add_resource(resources.UserLogoutRefresh, '/logout/refresh')
api.add_resource(resources.TokenRefresh, '/token/refresh')
api.add_resource(resources.CheckService, '/check_service')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, debug=False)
