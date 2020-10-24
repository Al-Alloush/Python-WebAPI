import uuid, os
from flask_restful import Resource, reqparse
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
        # check if username or email not exit.
        user = UserModel.find_user(data['username'], data['email']) 
        if user is not None:
            return {"message": "this user is existing before"}, 400

        user = UserModel(
            _id= str(uuid.uuid4()),
            username=data['username'],
            email=data['email'],
            password=data['password'],
            salt=str(os.urandom(32)),
            first_name="",
            last_name="",
            birthday=data['birthday'],
            userType=4,
            login_date= current_local_time(),
            acc_verified=False
        )
        try:
            user.save_to_db()
            check_user = UserModel.find_user(data['username'], data['email']) 
            if check_user is not None:
                return {"message": "add user successfully"}, 200
            
            return {"message": "somthing wrong!, please try again"}, 400
        except Exception as ex:
            return {"message": f"somthing wrong!"}, 500

