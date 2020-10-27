from models.User.UserModel import UserModel

class UserConfirmCRUD():
    
    @classmethod
    def update_acc_verified(cls, token):
        active = UserModel.activate_account(token)
        if active:
            return  {   "status": 200,
                        "message": "Account has been Activated successfully"
                    }
        else:
            return  {   "status": 401,
                        "message": "failed the Activation"
                    }