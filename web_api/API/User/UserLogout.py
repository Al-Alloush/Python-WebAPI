
from flask_jwt_extended import(
    get_raw_jwt, jwt_required
) 
from flask_restful import Resource
from dbs_connections.redis_db import revoked_store
from datetime import timedelta


class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']  # jti is "JWT ID", a unique identifier for a JWT.
        revoked_store.set("token_black_list:"+jti, 'true', timedelta(days = 30) * 1.2)
        return {"message": "Successfully logged out"}, 200