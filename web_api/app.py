import uuid, os
from app_production_settings import *
from flask import Flask, render_template
from flask_restful import Resource, Api
from resources.sql_db_alchemy import db
from models.User.UserModel import UserModel
from API.User.UserLogin import UserLogin
from API.User.UserRegister import UserRegister
from resources.global_functions import (
    hashing_text, current_local_time
)



app = Flask(__name__)
app.secret_key = APP_SECRET_KEY
''' to avoid error: ModuleNotFoundError: No module named 'MySQLdb'
    need to install pymysql library to update/add 'MySQLdb' module'''
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
''' flask-SQLAlchemy tracking every change that made to the SQLAlchemy session, and that took some resources. 
    And SQLAlchemy the main library itself has its own modification tracker which is a bit better.
    this is only changing the flask-SQLAlchemy extensions behaviours not SQLAlchemy. '''
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)

api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')


@app.before_first_request
def create_tables():
    db.create_all()
    username = "Al-Alloush"
    email = "ahmad@al-alloush.com"
    salt = str(os.urandom(32))
    userType = 1 #SuberAdmin
    current_time = current_local_time()
    existUser = UserModel.find_user(username, email)
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
            acc_verified= True  )
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