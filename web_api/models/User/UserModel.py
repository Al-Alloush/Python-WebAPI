import datetime, uuid, time
#
from resources.sql_db_alchemy import db
from resources.global_functions import (
    current_local_time
)

# ---------------------------

class UserModel(db.Model):
    # Create the user table
    # definition of the table to work with
    # table name.
    __tablename__ = 'users'
    # Table's columns.
    id = db.Column(db.String(80), primary_key=True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(500))
    salt = db.Column(db.String(500), unique=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name  = db.Column(db.String(80), nullable=False)
    birthday  = db.Column(db.DateTime)
    userType = db.Column(db.Integer)
    login_date  = db.Column(db.DateTime)
    acc_verified = db.Column(db.Boolean, default=False)
    register_date = db.Column(db.DateTime, default=current_local_time())
    token = db.Column(db.String(500))

    def __init__(self, _id, username, email, password, salt, first_name, last_name, birthday, userType, login_date, acc_verified, token):
        self.id = _id
        self.username = username
        self.email = email
        self.password = password
        self.salt = salt
        self.first_name = first_name
        self.last_name = last_name
        self.birthday = birthday
        self.userType = userType
        self.login_date = login_date
        self.acc_verified = acc_verified
        self.token = token


    @classmethod
    def find_user(cls, username, email):
        try:
            # check if user email or username exist
            user = cls.query.filter_by(username=username).first() # SELECT * FROM users WHERE username = username LIMIT 1"
            if user is None:
                user = cls.query.filter_by(email=email).first() # SELECT * FROM users WHERE email = email LIMIT 1"
        
        
            # if user exist return the user else return None
            return user
        except Exception as ex:
            return None
       
    @classmethod
    def activate_account(cls, token):
        try:
            user = cls.query.filter_by(token=token).first() # SELECT * FROM users WHERE token = token LIMIT 1"
            user.acc_verified = True
            user.save_to_db()
            return True
        except Exception as ex:
            return False

        return False

    def save_to_db(self):
        # add function work for both the insert and the update, updae if retrive an Id
        db.session.add(self)
        db.session.commit()


