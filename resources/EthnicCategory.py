from datetime import datetime

from flask_restful import Resource

import validation
from models.EthinicCategoryModel import CategoryModel


class EthnicCategory(Resource):
    def post(self):
        data = validation.category_create_validate().parse_args()
        category = CategoryModel()
        category.name = data['name'].lower()
        category.createdOn = datetime.now().isoformat()
        try:
            category.save_to_db()
            return {'message': 'Created {}'.format(category.id)}, 201
        except Exception as e:
            return {'message': 'Unable to Create {}'.format(e)}, 400

    def get(self):
        categories = CategoryModel.get_categories()
        return categories, 201


class EthnicCategoryByID(Resource):
    def get(self, _id):
        try:
            response = CategoryModel.get_ethnic_category_by_id(_id)
            return response, 201
        except Exception as e:
            return {'message': 'Server error {}'.format(e)}, 400
