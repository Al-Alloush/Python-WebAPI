from models.User.UserModel import UserModel
from resources.global_functions import(
    hashing_text, verify_password
)
from flask_jwt_extended import(
    create_access_token,  create_refresh_token, get_jti
)
from datetime import timedelta
from dbs_connections.redis_db import revoked_store

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


        # Store the tokens in redis with a status of not currently revoked. We
        # can use the `get_jti()` method to get the unique identifier string for
        # each token. We can also set an expires time on these tokens in redis,
        # so they will get automatically removed after they expire. We will set
        # everything to be automatically removed shortly after the token expires
        access_jti = get_jti(encoded_token=access_token) # get the curent id of the access Token
        refresh_jti = get_jti(encoded_token=refresh_token) # get the curent id of the refresh access Token
        revoked_store.set("token_black_list:"+access_jti, 'false', timedelta(minutes = 15) * 1.2)
        revoked_store.set("token_black_list:"+refresh_jti, 'false',  timedelta(days = 30)  * 1.2)

        return {
                "status": 200,
                "message": "Login Success",
                "username": user.username,
                "email": user.email,
                'access_token': access_token,
                'refresh_token': refresh_token
            }

