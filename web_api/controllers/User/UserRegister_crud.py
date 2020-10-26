import os, uuid
from models.User.UserModel import UserModel
from resources.global_functions import (
    hashing_text, current_local_time, valid_email,
    valid_password
)

class UserRegisterCRUD():

    def __init__(self, username, email, password, birthday):
        self.username = username
        self.email = email
        self.password = password
        self.birthday = birthday

    def create(self):
        if not valid_email(self.email):
            return  {   "status": 401,
                        "message": "email is not valid"
                    }
        # if valid return True, else retrun json
        valid_pass = valid_password(self.password)
        if valid_pass is not True:
            # if password not valid retrun error message with status: 401
            return valid_pass


        # check if username or email not exit.
        user = UserModel.find_user(self.username, self.email) 
        if user is not None:
            return  {   "status": 400,
                        "message": "this user is existing before"
                    }


        user = UserModel(
            _id= str(uuid.uuid4()),
            username=self.username,
            email=self.email,
            password=self.password,
            salt=str(os.urandom(32)),
            first_name="",
            last_name="",
            birthday=self.birthday,
            userType=4,
            login_date= current_local_time(),
            acc_verified=False
        )
        try:
            user.save_to_db()
            check_user = UserModel.find_user(self.username, self.email) 
            if check_user is not None:
                return  {   "status": 200,
                            "message": "Add user successfully"
                        }

            return  {   "status": 400,
                        "message": "Something wrong!, please try again"
                    }
        except :
            return  {   "status": 500,
                        "message": "Something wrong!, please call the support"
                    }