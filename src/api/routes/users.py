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
        return response_with(resp.SUCCESS_201, value={"author":
    result})
     
     except Exception as e:
         
         pass
         
         return response_with(resp.INVALID_INPUT_422)
     