from models.User.UserModel import UserModel
from flask_restful import Resource
from flask_jwt_extended import(
    jwt_required, get_jwt_identity, get_jwt_claims, fresh_jwt_required
) 

from resources.jwt_modify_functions import make_secure

class TestAuthentecation(Resource):
    # Get this functionality if the authorization token is validated
    # this decorator is for fresh or non-fresh asccess token
    @jwt_required
    @make_secure(4)
    def get (self):
        id =get_jwt_identity()
        user = UserModel.find_user(get_jwt_identity())# get the identity from access tocken, here is user.id
        return {"message": f" get with Authentecation successfully: {user.username}"}, 201

    # this decorator is for just for fresh asccess token, for example to change password we need a 
    @fresh_jwt_required
    @make_secure(4)
    def post(slef):
        id =get_jwt_identity()
        user = UserModel.find_user(get_jwt_identity())# get the identity from access tocken, here is user.id
        return {"message": f"get inside this post just after login and get a fresh token: {user.username}"}, 201

    @jwt_required
    @make_secure(2)
    def put(slef):
        # this function just for users permations
        id =get_jwt_identity()
        user = UserModel.find_user(get_jwt_identity())# get the identity from access tocken, here is user.id
        return {"message": f"this function just for users permations: {user.username}"}, 201

    
    @fresh_jwt_required
    @make_secure(1)
    def delete(slef):
        # this function just for Admin permations
        id =get_jwt_identity()
        user = UserModel.find_user(get_jwt_identity())# get the identity from access tocken, here is user.id
        return {"message": f"this function just for SuberAdmin permations: {user.username}"}, 201