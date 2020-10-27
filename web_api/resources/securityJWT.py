
'''
this file if use flask_jwt library
'''

from werkzeug.security import safe_str_cmp # safe string compare
from models.User.UserModel import UserModel as User
from resources.global_functions import verify_password

# in 
def authenticate(username, password):
    # it does not matter if passed username or email to this method
    user = User.find_user(username)
    # compare if password is right
    if user and verify_password(user.password, user.salt, password):
        return user

def identity(payload):
    user_id = payload['identity']
    return User.find_by_id(user_id)