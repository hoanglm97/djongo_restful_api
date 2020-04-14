from flask import Flask, escape, request

from app import app

app.run(host="0.0.0.0", debug=True)
