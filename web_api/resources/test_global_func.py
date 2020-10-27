import pytest, os
from resources.global_functions import(
    valid_email, valid_password, verify_password, hashing_text, current_local_time
)

def test_valid_email():
    assert valid_email("ksjdf@lsdkf.com") == True
    assert valid_email("ksjdfsdkf.com") == False

def test_valid_password():
    assert valid_password("sdfgdfdfg") == False
    assert valid_password("!QA1qa") == True

def test_verify_password():
    password = "sdfgl/s§D23"
    salt = str(os.urandom(32))
    hashPass = hashing_text(password,salt)
    assert verify_password(hashPass,salt,password) == True
    password = "!QA1qa"
    assert verify_password(hashPass,salt,password) == False

