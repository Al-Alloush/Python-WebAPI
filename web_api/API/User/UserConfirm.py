from flask_restful import Resource, reqparse
from controllers.User.userConfirm_crud import UserConfirmCRUD as uc_crud


class UserConfirm(Resource):
    @classmethod
    def get(cls, token):
        activate = uc_crud.update_acc_verified(token)
        if activate:
            headers = {"Content-Type": "text/html"}
            return {"message": 'confirm email successfully'}, 200
  
        return {"message": "failed to confirm email"}, 500