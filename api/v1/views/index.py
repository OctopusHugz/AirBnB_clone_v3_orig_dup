#!/usr/bin/python3
""" views routes """
from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage


@app_views.route("/status")
def stats():
    """ returns the status """
    newdict = {
        "status": "OK"
    }
    return newdict

@app_views.route("/stats")
def class_stats():
    """ endpoint that gets the stats of each obj """
    all_stats = {
        'amenities': storage.count('Amenity'),
        'cities': storage.count('City'),
        'places': storage.count('Place'),
        'reviews': storage.count('Review'),
        'states': storage.count('State'),
        'users': storage.count('User')
    }
    return jsonify(all_stats)
