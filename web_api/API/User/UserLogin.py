
from flask import request, url_for
from flask_restful import Resource, reqparse
from controllers.User.UserLogin_crud import UserLoginCRUD as ul_crud 

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

        user = ul_crud(data["usernameOrEmail"], data["password"])
        login = user.read()
        return login, login["status"]
        