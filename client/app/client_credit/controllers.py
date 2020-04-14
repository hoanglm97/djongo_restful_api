# import smt important that maybe you need
from flask import (
    request,
    Blueprint,
    session,
    redirect,
    flash
)
from app import db
from app import jsonrpc
from app import app
from datetime import datetime, timedelta, time
# import fields from clientCredit models
from app.client_credit.models import ClientCredit

# from flask_restful import reqparse
# import flask from Flask 
from flask import Flask

# sqlalchemy check error
from sqlalchemy.exc import IntegrityError

# return to jsonrpc if error
from flask_jsonrpc.exceptions import Error

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode

credit = Blueprint("client", __name__, url_prefix="/client")



@jsonrpc.method("client.credit")
def count_cash(is_active, email, create_time, end_time, total_used, used_per_hour):
    total_time = 0
    # get data from request
    email = request.args.get("email")
    create_time = request.args.get("create_time")
    is_active = request.args.get("is_active")
    active = ClientCredit.find_by_active_status(is_active)
    client = ClientCredit.find_by_email(email)
    if active:
        try:
            if not client:
                return {
                    "message": "User does not exist"
                }, 404
            else:
                # caculate time what client used
                start = create_time.strptime("%m/%d/%Y, %H:%M:%S")
                end = end_time.strptime("%m/%d/%Y, %H:%M:%S")
                total_time = int(end - start)
                print("Total time used: {}".format(total_time))
                result = total_time * total_used
                total = 0
                if result:
                    total = used_per_hour * result
                else:
                    return {
                        "message": "Client haven't uset yet!"
                        }, 417
        except Exception as error:
            flash("Error: {}".format(error), "error")
    else:
        print("Check active user!")
        return {
            "message": "This account is not active!"
        }
        