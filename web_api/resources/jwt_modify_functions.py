

import functools
from models.User.UserModel import UserModel
from flask_jwt_extended import get_jwt_identity

def make_secure(userType):
    def decorator(func):
        @functools.wraps(func)
        def secure_function(*args, **kwargs):
            id =get_jwt_identity()
            user = UserModel.find_user(get_jwt_identity())# get the identity from access tocken, here is user.id
            if user.userType <= userType:
                return func(*args, **kwargs)
            else:
                return f"No {userType} permissions for {user.username}."
        return secure_function
    return decorator