from flask import request, jsonify
from app import db
from . import api
from ..models import User,user_schema

# Create a user
@api.route('/user', methods=['POST'])
def add_user():
    new_user = user_schema.load(request.json)
    db.session.add(new_user)
    db.session.commit()
    return user_schema.jsonify(new_user)

# Get all users
@api.route('/user', methods=['GET'])
def get_users():
    all_users = User.query.all()
    result = user_schema.dump(all_users,many=True)
    return jsonify(result)

# Get a single user
@api.route('/user/<int:id>', methods=['GET'])
def get_user(id):
    
    user = User.query.get(id)

    return user_schema.jsonify(user)           

# Update a user
@api.route('/user/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get(id)
    user = user_schema.load(request.json,instance=user,partial=True)

    db.session.commit()

    return user_schema.jsonify(user)

# Delete user

@api.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)

    db.session.commit()

    return user_schema.jsonify(user)

