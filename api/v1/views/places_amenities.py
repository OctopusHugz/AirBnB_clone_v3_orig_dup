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


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 strict_slashes=False, methods=['GET', 'POST'])
def place_amenities(place_id, amenity_id):
    """ /places/<place_id>/amenities route """
    amenity_list = []
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is not None:
        if models.storage_t != 'db':
            amenities = place.amenity_ids
        else:
            amenities = place.amenities
        if request.method == 'GET':
            for amen in amenities:
                amenity_list.append(amen.to_dict())
            return jsonify(amenity_list)
        elif request.method == 'POST':
            try:
                if storage.get(Place, place_id) is None:
                    return {"error": "Not found"}, 404
                if storage.get(Amenity, amenity_id) is None:
                    return {"error": "Not found"}, 404
                if amenity_id in amenities:
                    return jsonify(amenity.to_dict()), 200
                return jsonify(amenity.to_dict()), 201
            except:
                return {"error": "Not a JSON"}, 400
    return {"error": "Not found"}, 404


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 strict_slashes=False, methods=['DELETE'])
def place_amenity_id(place_id, amenity_id):
    """ /places/<place_id>/amenities/<amenity_id> route """
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is not None:
        if models.storage_t != 'db':
            amenities = place.amenity_ids
        else:
            amenities = place.amenities
        if amenity is not None and amenity in amenities:
            if request.method == 'DELETE':
                storage.delete(amenity)
                storage.save()
                return {}, 200
    return {"error": "Not found"}, 404
