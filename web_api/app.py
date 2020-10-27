import uuid, os
from datetime import timedelta
from app_production_settings import *
from flask import Flask, render_template, jsonify
from flask_restful import Resource, Api
from dbs_connections.sql_db_alchemy import db
from models.User.UserModel import UserModel
from API.User.UserLogin import UserLogin
from API.User.UserRegister import UserRegister
from API.User.UserConfirm import UserConfirm
from API.User.UserLogout import UserLogout
from API.TestAuthentecation import TestAuthentecation
from resources.global_functions import (
    hashing_text, current_local_time
)
from flask_jwt_extended import(
    JWTManager
) 
from dbs_connections.redis_db import revoked_store



app = Flask(__name__)
app.secret_key = APP_SECRET_KEY
''' to avoid error: ModuleNotFoundError: No module named 'MySQLdb'
    need to install pymysql library to update/add 'MySQLdb' module'''
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
''' flask-SQLAlchemy tracking every change that made to the SQLAlchemy session, and that took some resources. 
    And SQLAlchemy the main library itself has its own modification tracker which is a bit better.
    this is only changing the flask-SQLAlchemy extensions behaviours not SQLAlchemy. '''
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes = 15) 
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days = 30)  
app.config['JWT_BLACKLIST_ENABLED'] = True # enable blacklist feature
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh'] # allow blacklisting for access and refresh tokens


api = Api(app)
'''
if use flask_jwt library:
JWT provide an auth endpoint to verify the user, with this login return a token, 
this token contains the user's Id and authentication code
jwt = JWT(app, authenticate, identity)'''
# flask_jwt_extended library
jwt = JWTManager(app)


# add claims to access token
@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    user = UserModel.find_user(identity)
    return {
        "username":user.username,
        "email": user.email
    }

# configer the message it should send back to the user telling it that their token has expired.
# The following callbacks are used for customizing jwt response/error messages.
# The original ones may not be in a very pretty format (opinionated)
@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'description': 'The token has expired.',
        'error': 'token_expired'
    }), 401

# it's going be called when the token, that sent in the Authorization header is not an actual JWT.
@jwt.invalid_token_loader
def invalid_token_callback(error):  # we have to keep the argument here, since it's passed in by the caller internally
    return jsonify({
        'description': 'Signature verification failed.',
        'error': 'invalid_token'
    }), 401

# it's going to be called when clint don't send an Authorization JWT at all.
@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        'description': 'Request does not contain an access token.',
        'error': 'authorization_required'
    }), 401

# functions need a fresh Token, if clint send a non-fresh token call this function.
@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return jsonify({
        'description': 'The token is not fresh.',
        'error': 'fresh_token_required'
    }), 401

# when user log out in token lifetime, set this token is revoked, then clint can't call fuctions with old Token.
@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        'description': 'The token has been revoked.',
        'error': 'token_revoked'
    }), 401 
# This method will check if a token is blacklisted, and will be called automatically when blacklist is enabled
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    entry = revoked_store.get("token_black_list:"+jti)
    if entry is None:
        return True
    return entry == 'true'



api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(UserConfirm, '/userconfirm/<string:token>')
api.add_resource(TestAuthentecation, '/TestAuthentecation')


# to create all tables with the first requst in app and add the SuperAdmin user
@app.before_first_request
def create_tables():
    db.create_all()
    username = "Al-Alloush"
    email = "ahmad@al-alloush.com"
    salt = str(os.urandom(32))
    token = hashing_text(str(uuid.uuid4), salt) 
    userType = 1 #SuberAdmin
    current_time = current_local_time()
    # check if username or email not exit.
    existUser = UserModel.find_user(username) 
    if existUser is None:
        existUser = UserModel.find_user(email) 
    if existUser is None:
        
        user = UserModel(
            _id= str(uuid.uuid4()),
            username= username,
            email= email,
            password= hashing_text("!QA1qa", salt), 
            salt= salt,
            first_name= "Ahmad",
            last_name="Alloush",
            birthday= "1979-5-5",
            userType= userType,
            login_date= current_time,
            acc_verified= True,
            token=token
            )
        try:
            user.save_to_db()
            return {"message": "User created successfully."}, 201
        except Exception as ex:
            return {"message": "Servir Error"}, 500

# dockerater
@app.route('/')
def home():
    return render_template("index.html")


if __name__ == '__main__':
    db.init_app(app)
    app.run(port="5000", host="0.0.0.0") # http://localhost:5000