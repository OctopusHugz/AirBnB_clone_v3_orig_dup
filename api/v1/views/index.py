#!/usr/bin/python3
""" views routes """
from api.v1.views import app_views
from flask import Flask, jsonify

@app_views.route("/status")
def stats():
    """ returns the status """
    newdict = {
        "status": "OK"
    }
    return newdict
