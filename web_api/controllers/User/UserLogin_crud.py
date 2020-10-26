from models.User.UserModel import UserModel
from resources.global_functions import(
    hashing_text, verify_password
)

class UserLoginCRUD():

    def __init__(self, usernameOrEmail, password):
        self.usernameOrEmail = usernameOrEmail
        self.password = password


    def read(self):

        user = UserModel.find_user(self.usernameOrEmail, self.usernameOrEmail)
        if user is None:
            return  {   "status": 401,
                        "message": "This user not exist"
                    }

        success = verify_password(user.password, user.salt, self.password)
        if not success:
            return  {   "status": 401,
                        "message": "username or password was wrong!, please try agian"
                    }

        return  {"status": 200,
                 "message": "Login Success"
                }