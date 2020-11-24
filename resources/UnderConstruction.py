from flask import make_response, render_template
from flask_restful import Resource


class UnderConstruction(Resource):
    def get(self):
        return make_response(render_template('under_construction.html'))
