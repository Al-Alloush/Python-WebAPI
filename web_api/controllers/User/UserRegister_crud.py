import os, uuid
from flask import request, url_for
from resources.sender import EmailSender
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
        if not valid_pass:
            # if password not valid retrun error message with status: 401
            return {"status": 401,
                    "message":  "password must be longer than 5 and less than 18,\
                    must contain at least one number, one uppercase letter, \
                    one lowercase letter, and one punctuation"
                    }


        # check if username or email not exit.
        user = UserModel.find_user(self.username) 
        if user is None:
            user = UserModel.find_user( self.email) 
        if user is not None:
            return  {   "status": 400,
                        "message": "this user is existing before"
                    }

        salt = str(os.urandom(32))
        token = str(hashing_text(str(uuid.uuid4), salt))
        user = UserModel(
            _id= str(uuid.uuid4()),
            username=self.username,
            email=self.email,
            password=hashing_text(self.password, salt),
            salt=salt,
            first_name="",
            last_name="",
            birthday=self.birthday,
            userType=4,
            login_date= current_local_time(),
            acc_verified=False,
            token=token
        )
        try:
            user.save_to_db()
            check_user = UserModel.find_user(self.username) 
            if check_user is not None:
                # the url of app lik: http://localhost:5000
                link = request.url_root[:-1] + url_for("userconfirm", token=token)
                SenderEmail = EmailSender(
                    user.email,
                    "Activation account",
                    "please click at the next link to Activing your account:</br>"+ link
                    )
                SenderEmail.send()

                return  {   "status": 200,
                            "message": "Add user successfully, please check your email to Activate this account"
                        }

            return  {   "status": 400,
                        "message": "Something wrong!, please try again"
                    }
        except Exception as ex :
            return  {   "status": 500,
                        "message": "Something wrong!, please call the support, ERROR="+ str(ex)
                    }