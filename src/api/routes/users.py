from flask import Blueprint, request, url_for, render_template_string
from flask_jwt_extended import create_access_token, jwt_required

from api.utils.database import db
from api.models.users import User, UserSchema
from api.utils.responses import response_with
from api.utils import responses as resp
from api.utils.token import generate_verification_token, confirm_verification_token
from api.utils.email import send_email



user_routes = Blueprint("user_routes", __name__)

# create user
@user_routes.route('/create_user', methods=['POST'])
#@jwt_required
def create_user():
     try:
        data = request.get_json()
        # data['password_hash'] = User.generate_hash(data['password'])
        user_schema = UserSchema()
        user, error = user_schema.load(data)
        result = user_schema.dump(user.create()).data
        return response_with(resp.SUCCESS_201, value={"user":
    result})
     
     except Exception as e:
         print(e)
         return response_with(resp.INVALID_INPUT_422)
     
# Get users endpoint
@user_routes.route('/get_users', methods=['GET'])
def get_users():
    fetched = User.query.all()
    user_schema = UserSchema(many=True, only=['fullname', 'email', 'id'])
    users, error = user_schema.dump(fetched)
    return response_with(resp.SUCCESS_200, value={"users": users})

# Get specific user using their ID
@user_routes.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    fetched = User.query.get_or_404(user_id)
    user_schema = UserSchema
    user, error = user_schema.dump(fetched)
    return response_with(resp.SUCCESS_200, value={"user": user})

# update user
@user_routes.route('/<int:id>', methods=['PUT'])
def update_user_detail(id):
    data = request.get_json()
    get_user = user.query.get_or_404(id)
    get_user.fullname = data['fullname']
    db.session.add(get_user)
    db.session.commit()
    user_schema = UserSchema()
    user, error = user_schema.dump(get_user)
    return response_with(resp.SUCCESS_200, value={"user":
    user})

# update only a part of the user object
@user_routes.route('/<int:id>', methods=['PATCH'])
def modify_user_detail(id):
    data = request.get_json()
    get_user = User.query.get(id)
    if data.get('fullname'):
        get_user.fullname = data['fullname']
    if data.get('email'):
        get_user.email = data['email']
    db.session.add(get_user)
    db.session.commit()
    user_schema = UserSchema
    user, error = user_schema.dump(get_user)
    return response_with(resp.SUCCESS_200, value={"user": user})

# delete user
@user_routes.route('/<int:id>', methods=['DELETE'])
def delete_user(id):
    get_user = User.query.get_or_404(id)
    db.session.delete(get_user)
    db.session.commit()
    return response_with(resp.SUCCESS_204)

# validate user email
@user_routes.route('/confirm/<token>', methods=['GET'])
def verify_email(token):
    try:
        email = confirm_verification_token(token)
    except:
        return response_with(resp.SERVER_ERROR_404)
        user = User.query.filter_by(email=email).first_or_404()
        if user.isVerified:
            return response_with(resp.INVALID_INPUT_422)
        else:
            user.isVerified = True
            db.session.add(user)
            db.session.commit()
            return response_with(resp.SUCCESS_200, value={"message":
            "Email verified, you can now login."})

# login user
@user_routes.route('/login', methods=['POST'])
def authenticate_user():
    try:
        data = request.get_json()
        # The user to send the email address in login endpoint , and if the user isn’t verified,
        # return the request with a 400 bad code without the token.
        current_user = User.find_by_email(data['email'])
        if not current_user:
             return response_with(resp.SERVER_ERROR_404)
        if User.verify_hash(data['password_hash'], current_user.password_hash):
                access_token = create_access_token(identity =
                data['email'])
                return response_with(resp.SUCCESS_201, value={'message': 'Logged in as {}'.format(current_user.email), "access_token": access_token})
        else:
                return response_with(resp.UNAUTHORIZED_401)
    except Exception as e:
            #print e
            return response_with(resp.INVALID_INPUT_422)
    



