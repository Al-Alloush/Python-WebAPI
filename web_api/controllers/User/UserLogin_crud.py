from models.User.UserModel import UserModel
from resources.global_functions import(
    hashing_text, verify_password
)
from flask_jwt_extended import(
    create_access_token,  create_refresh_token
)

class UserLoginCRUD():

    def __init__(self, usernameOrEmail, password):
        self.usernameOrEmail = usernameOrEmail
        self.password = password


    def read(self):

        user = UserModel.find_user(self.usernameOrEmail)
        if user is None:
            return  {   "status": 401,
                        "message": "This user not exist"
                    }

        success = verify_password(user.password, user.salt, self.password)
        if not success:
            return  {   "status": 401,
                        "message": "username or password was wrong!, please try agian"
                    }

        # check if user Activate his Account or not
        if user.acc_verified is False:
            return  {   "status": 401,
                        "message": "please check your email and Activate your Account"
                    }

        # identity= is what the identity() function did in securityJWT.py, now stored in the JWT
        access_token = create_access_token(identity=user.username, fresh=True) 
        refresh_token = create_refresh_token(user.id)

        return {
                "status": 200,
                "message": "Login Success",
                "username": user.username,
                "email": user.email,
                'access_token': access_token,
                'refresh_token': refresh_token
            }

