from flask import Blueprint
from flask import request
from api.utils.responses import response_with
from api.utils import responses as resp

from api.models.users import User, UserSchema
from api.utils.database import db

user_routes = Blueprint("user_routes", __name__)

@user_routes.route('/', methods=['POST'])
def create_user():
     try:
        data = request.get_json()
        user_schema = UserSchema()
        user, error = user_schema.load(data)
        result = user_schema.dump(user.create()).data
        return response_with(resp.SUCCESS_201, value={"user":
    result})
     
     except Exception as e:
         
         pass
         
         return response_with(resp.INVALID_INPUT_422)

@user_routes.route('/<int:id>', methods=['PUT'])
def update_user_detail(id):
    data = request.get_json()
    get_user = user.query.get_or_404(id)
    get_user.first_name = data['first_name']
    get_user.last_name = data['last_name']
    db.session.add(get_user)
    db.session.commit()
    user_schema = UserSchema()
    user, error = user_schema.dump(get_user)
    return response_with(resp.SUCCESS_200, value={"user":
    user})