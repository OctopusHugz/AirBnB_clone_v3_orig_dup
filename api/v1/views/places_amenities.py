#!/usr/bin/python3
""" places routes """
from models.place import Place
from models.review import Review
from models.amenity import Amenity
from models.city import City
from os import getenv
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import jsonify, request


@app_views.route("/places/<place_id>/amenities", strict_slashes=False,
                 methods=['GET', 'POST'])
def amenities(place_id):
    """ /places/<place_id>/amenities route """
    amenity_list = []
    place = storage.get(Place, place_id)
    if place is not None:
        amenities = place.amenities
        if request.method == 'GET':
            if getenv('HBNB_TYPE_STORAGE') != 'db':
                return jsonify(place.amenity_ids)
            else:
                for amenity in amenities:
                    amenity_list.append(amenity.to_dict())
                    return jsonify(amenity_list)
        elif request.method == 'POST':
            try:
                new_dict = request.get_json()
                if storage.get(Place, new_dict['place_id']) is None:
                    return 404
                if storage.get(Amenity, new_dict['amenity_id']) is None:
                    return 404
                new_dict.update({'amenity_id': amenity_id})
                new_inst = Amenity(**new_dict)
                new_inst.save()
                if getenv('HBNB_TYPE_STORAGE') != 'db':
                    return jsonify(new_inst), 201
                else:
                    return jsonify(new_inst.to_dict()), 201
            except:
                return 404
    return 404


@app_views.route("/places/<place_id>/amenities/<amenity_id>", strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def amenity_id(amenity_id):
    """ /places/<place_id>/amenities/<amenity_id> route """
    ignore_list = ["id", "user_id", "place_id", "created_at", "updated_at"]
    amenity = storage.get(Amenity, amenity_id)
    if amenity is not None:
        if request.method == 'GET':
            if getenv('HBNB_TYPE_STORAGE') != 'db':
                return jsonify(amenity)
            else:
                return jsonify(amenity.to_dict())
        elif request.method == 'DELETE':
                storage.delete(amenity)
                storage.save()
                return jsonify({}), 200
        elif request.method == 'PUT':
            try:
                new_dict = request.get_json()
                if getenv('HBNB_TYPE_STORAGE') != 'db':
                    for key, value in amenity.items():
                        if key not in ignore_list:
                            amenity.update({key: value})
                            storage.delete(amenity)
                            storage.new(Amenity(**amenity))
                            storage.save()
                            return jsonify(amenity), 200
                else:
                    amenity_dict = amenity.to_dict()
                    for key, value in amenity_dict.items():
                        if key not in ignore_list:
                            amenity_dict.update({key: value})
                            storage.delete(amenity)
                            storage.new(Amenity(**amenity_dict))
                            storage.save()
                            return jsonify(amenity_dict), 200
            except:
                return {"error": "Not a JSON"}, 400
    return {"error": "Not found"}, 404
