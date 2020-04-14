# Import flask dependencies
from flask import (
    Blueprint,
    request,
    render_template,
    flash,
    g,
    session,
    redirect,
    url_for,
)


from werkzeug.security import check_password_hash, generate_password_hash
from app import db
from app import jsonrpc
from app import app

# use fernet to encrypt passsword
# origin :
from cryptography.fernet import Fernet
from flask_cors import CORS, cross_origin
from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple
from app.mod_auth.models import User
from flask import Flask
import pprint

#  sql check error
from sqlalchemy.exc import IntegrityError

# write code return to rpc json
from flask_jsonrpc.exceptions import Error

auth_module = Blueprint("auth", __name__)
key = app.config["FERNET_KEY"].encode("utf-8")


# CORS(auth_module)

#  docss : https://json-rpc.readthedocs.io/en/latest/flask_integration.html


@jsonrpc.method("auth.register")
def register(username, email, password):
    try:
        # passsword_byte = password.encode("utf-8")
        # cipher_suite = Fernet(key)
        # ciphered_text = cipher_suite.encrypt(passsword_byte)
        new_user = User(username, email, password, 0, 0)
        db.session.add(new_user)
        db.session.commit()
        return "Success"
    except:
        error = Error(message="Email đã tồn tại")
        raise error


@jsonrpc.method("auth.login")
def login(email, password):
    print(password)
    # user = User.query.filter_by(email=email).first()
    # try:
    #     if user.password == password:
    #         return "Login sucess"
    #     else:
    #         error = Error(message="Thông tin đăng nhập thông chính xác")
    #         raise error
    # except:
    #     error = Error(
    #         message="Thông tin đăng nhập không chính xác. Mật khẩu của bạn là "
    #         + user.password
    #     )
    #     raise error
