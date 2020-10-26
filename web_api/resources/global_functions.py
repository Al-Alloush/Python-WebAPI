import hashlib, os, re, string as st, time
from werkzeug.security import safe_str_cmp # safe string compare
from datetime import datetime

def valid_email(email):
    ''' check if the email is valid'''
    if re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return True
    return False
    

def valid_password(password):
    ''' check if the password is valid.
        password must be longer than 5 and less than 18,
        must contain at least one number, one uppercase letter, 
        one lowercase letter, and one punctuation:
    '''
    if  len(password) < 6 or \
        len(password) > 18 or \
        len(set(st.digits).intersection(password)) <= 0 or \
        len(set(st.ascii_lowercase).intersection(password)) <= 0 or \
        len(set(st.ascii_uppercase).intersection(password)) <= 0 or \
        len(set(st.punctuation).intersection(password)) <= 0 :
        return {"status": 401,
                "message":  "password must be longer than 5 and less than 18,\
                must contain at least one number, one uppercase letter, \
                one lowercase letter, and one punctuation"
                }
    return True

def verify_password(hashed_password, stored_salt, password):
    ''' Verify a stored password against one provided by user
        Parameters:
            hashed_password : str
                The hashed_password stored in database
            stored_salt : str
                The salt has stored in databse
            password : str
                the password
    '''
    new_key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), stored_salt.encode('utf-8'), 100000)
    return safe_str_cmp(str(hashed_password) ,str(new_key))

def hashing_text(text, salt):
    ''' Hash a text.
        Parameters:
            text : str
                The string like password
            salt : str
                The slat to hash the text
    '''
    key = hashlib.pbkdf2_hmac('sha256', text.encode('utf-8'), salt.encode('utf-8'), 100000)
    return str(key)

def current_local_time():
    ''' retrun the current local time.
        return type: string.
    '''
    now_date_time = datetime.utcnow()
    now_timestamp = time.time()
    offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(now_timestamp)
    current_time = now_date_time + offset
    return  current_time.strftime('%Y-%m-%d %H:%M:%S')