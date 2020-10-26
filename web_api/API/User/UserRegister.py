import uuid, os
from flask_restful import Resource, reqparse
from controllers.User.UserRegister_crud import UserRegisterCRUD as ur_crud
from models.User.UserModel import UserModel
from resources.global_functions import (
    hashing_text, current_local_time
)

class UserRegister(Resource):
    TABLE_NAME = 'users'

    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="username field cannot be left blank!"
                        )
    parser.add_argument('email',
                        type=str,
                        required=True,
                        help="email field cannot be left blank!"
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="password field cannot be left blank!"
                        )
    parser.add_argument('birthday',
                        type=str,
                        required=True,
                        help="birthday field cannot be left blank!"
                        )

    def post(self):
        data = UserRegister.parser.parse_args()
        user = ur_crud(data["username"], data["email"], data["password"], data["birthday"])
        create = user.create()
        return create, create["status"]
            


