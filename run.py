import os

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api

from models.RevokedTokenModel import RevokedTokenModel
from resources.UnderConstruction import UnderConstruction
from resources.CheckService import TokenRefresh, CheckService
from resources.EthnicCategory import EthnicCategory, EthnicCategoryByID
from resources.MainRoute import MainRoute
from resources.UserLogin import UserLogin
from resources.UserLogoutAccess import UserLogoutAccess
from resources.UserLogoutRefresh import UserLogoutRefresh
from resources.UserRegistration import UserRegistration

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
    return RevokedTokenModel.is_jti_blacklisted(jti)


api.add_resource(UnderConstruction, '/')
api.add_resource(MainRoute, '/swagger')
api.add_resource(UserLogin, '/login')
api.add_resource(UserRegistration, '/register')
api.add_resource(UserLogoutAccess, '/logout/access')
api.add_resource(UserLogoutRefresh, '/logout/refresh')
api.add_resource(TokenRefresh, '/token/refresh')
api.add_resource(CheckService, '/check_service')
api.add_resource(EthnicCategory, '/ethnicCategory')
api.add_resource(EthnicCategoryByID, '/ethnicCategory/<string:_id>')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, debug=False)
