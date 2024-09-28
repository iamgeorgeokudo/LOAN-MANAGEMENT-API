from flask import Blueprint
from flask import request
from api.utils.responses import response_with
from api.utils import responses as resp

from api.models.users import User, UserSchema
from api.utils.database import db
from flask_jwt_extended import create_access_token, jwt_required

user_routes = Blueprint("user_routes", __name__)

# create user
@user_routes.route('/', methods=['POST'])
@jwt_required
def create_user():
     try:
        data = request.get_json()
        data['password_hash'] = User.generate_hash(data['password_hash'])
        user_schema = UserSchema()
        user, error = user_schema.load(data)
        result = user_schema.dump(user.create()).data
        return response_with(resp.SUCCESS_201, value={"user":
    result})
     
     except Exception as e:
         
         pass
         
         return response_with(resp.INVALID_INPUT_422)

# login user
@user_routes.route('/login', methods=['POST'])
def authenticate_user():
    try:
        data = request.get_json()
        current_user = User.find_by_email(data['email'])
        if not current_user:
            return response_with(resp.SERVER_ERROR_404)
        if User.verify_hash(data['password_hash'], current_user.password_hash):
            access_token = create_access_token(identity =
            data['email'])

            return response_with(resp.SUCCESS_201, 
            value={'message': 'Logged in as {}'.format(current_user.email), "access_token": access_token})
        else:
            return response_with(resp.UNAUTHORIZED_401)
    except Exception as e:

        #print e

        return response_with(resp.INVALID_INPUT_422)


# update user
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