import os
from flakon import SwaggerBlueprint
#from flask import request
from beepbeep.dataservice.database import db, User, Run

HERE = os.path.dirname(__file__)
YML = os.path.join(HERE, '..', 'static', 'api-swagger.yaml')
users_api = SwaggerBlueprint('users', __name__, swagger_spec=YML)


@users_api.operation('getUsers')
def get_users():
    users = db.session.query(User)
    page = 0
    page_size = None
    if page_size:
        users = users.limit(page_size)
    if page != 0:
        users = users.offset(page * page_size)
    return {'users': [user.to_json(secure=True) for user in users]}

@users_api.operation('createUser')
def create_user():
    #request.json()
    users = db.session.query(User)
    page = 0
    page_size = None
    if page_size:
        users = users.limit(page_size)
    if page != 0:
        users = users.offset(page * page_size)
    return {'users': [user.to_json(secure=True) for user in users]}
