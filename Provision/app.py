
# import settings
# import os
# import re
# from bson.json_util import dumps as dumps_json
from flask import Flask, render_template, jsonify, Response, request
# from functools import wraps
# from write_file import grandstream, yeslink, atcom
# import redis
import sys
# import write_log_redis
# from hotqueue import HotQueue
# from raven import Client

app = Flask(__name__, static_folder='/data')


@app.route('/')
def hello_world():
    return render_template('errors.html', error='There are too many errors in this service :v')


if __name__ == '__main__':
    try:
        port = int(sys.argv[1])
    except (TypeError, IndexError):
        port = 9000
    app.run(host='127.0.0.1', port=port, debug=True)
