
from flask import request, url_for
from flask_restful import Resource, reqparse
from models.User.UserModel import UserModel
from resources.global_functions import(
    hashing_text, verify_password
) 

class UserLogin(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('usernameOrEmail',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    def post(self):
        data = UserLogin.parser.parse_args()

        user = UserModel.find_user(data['usernameOrEmail'], data['usernameOrEmail'])
        if user is None:
            return {"message": "This user not exist"}, 401

        success = verify_password(user.password, user.salt, data["password"])
        if not success:
            return {"message": "username or password was wrong"}, 401


        return {"message": "Login Success"}, 200