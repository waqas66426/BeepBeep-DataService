import os
from flakon import SwaggerBlueprint
from flask import request, jsonify
from beepbeep.dataservice.database import db, User, Run

HERE = os.path.dirname(__file__)
YML = os.path.join(HERE, '..', 'static', 'api-swagger.yaml')
users_api = SwaggerBlueprint('users', __name__, swagger_spec=YML)

def fill(source, target):
    for prop in source:
        setattr(target, prop, source[prop])

@users_api.operation('getUsers')
def get_users():
    users = db.session.query(User)
    page = 0
    page_size = None
    if page_size:
        users = users.limit(page_size)
    if page != 0:
        users = users.offset(page * page_size)
    return jsonify([user.to_json(secure=True) for user in users])


@users_api.operation('createUser')
def create_user():
    raw_user = request.get_json()

    if raw_user is None:
        return "Invalid user body", 400

    user = User()
    fill(raw_user, user)

    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Unknown error occurred"}), 500

    return jsonify(user.to_json()), 201

@users_api.operation('updateUserById')
def update_user_by_id(id):

    raw_user = request.get_json()

    if raw_user is None:
        return "Invalid user body", 400

    try:
        user = db.session.query(User).filter(User.id == id).first()
        fill(raw_user, user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Unknown error occurred"}), 500

    return jsonify(user.to_json()), 201



@users_api.operation('getUserById')
def get_user_by_id(id):
    if id is None:
        return "Invalid user id", 400

    try:
        user = db.session.query(User).filter(User.id == id).first()

        if(user is None):
            return jsonify({"error": "User not found"}), 404

        return jsonify(user.to_json()), 201
    except Exception as e:
        return jsonify({"error": "Unknown error occurred"}), 500



@users_api.operation('deleteUserById')
def delete_user_by_id(id):
    if id is None:
        return "Invalid user id", 400
    try:
        db.session.query(User).filter(User.id == id).delete()
        db.session.commit()
        return "", 204
    except Exception as e:
        return jsonify({"error": "Unknown error occurred"}), 500