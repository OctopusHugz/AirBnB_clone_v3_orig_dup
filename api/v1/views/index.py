#!/usr/bin/python3
""" views routes """
from models.user import User
from models.state import State
from models.review import Review
from models.place import Place
from models.city import City
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from flask import Flask, jsonify


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
        'amenities': storage.count(Amenity),
        'cities': storage.count(City),
        'places': storage.count(Place),
        'reviews': storage.count(Review),
        'states': storage.count(State),
        'users': storage.count(User)
    }
    return jsonify(all_stats)
