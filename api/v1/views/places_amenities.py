#!/usr/bin/python3
""" places routes """
import models
from models.place import Place
from models.review import Review
from models.amenity import Amenity
from models.city import City
from os import getenv
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import jsonify, request


@app_views.route("/places/<place_id>/amenities/",
                 strict_slashes=False, methods=['GET'])
def place_amenities(place_id):
    """ /places/<place_id>/amenities route """
    amenity_list = []
    place = storage.get(Place, place_id)
    if place is None:
        return {"error": "Not found"}, 404
    if models.storage_t != 'db':
        amenities = place.amenity_ids
    else:
        amenities = place.amenities
    if request.method == 'GET':
        for amenity in amenities:
            amenity_list.append(amenity.to_dict())
        return jsonify(amenity_list)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 strict_slashes=False, methods=['DELETE', 'POST'])
def place_amenity_id(place_id, amenity_id):
    """ /places/<place_id>/amenities/<amenity_id> route """
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None or amenity is None:
        return {"error": "Not found"}, 404
    if models.storage_t != 'db':
        amenities = place.amenity_ids
    else:
        amenities = place.amenities
    if request.method == 'DELETE':
        if amenity not in amenities:
            return {"error": "Not found"}, 404
        storage.delete(amenity)
        storage.save()
        return {}, 200
    elif request.method == 'POST':
        try:
            if amenity in amenities:
                return jsonify(amenity.to_dict()), 200
            amenities.append(amenity)
            return jsonify(amenity.to_dict()), 201
        except:
            return {"error": "Not a JSON"}, 400
