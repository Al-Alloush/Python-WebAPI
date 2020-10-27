from flask_restful import Resource, reqparse
from controllers.User.userConfirm_crud import UserConfirmCRUD as uc_crud


class UserConfirm(Resource):
    @classmethod
    def get(cls, token):
        activate = uc_crud.update_acc_verified(token)
        return activate, activate["status"]