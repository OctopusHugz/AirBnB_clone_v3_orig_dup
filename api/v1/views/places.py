#!/usr/bin/python3
""" places routes """
from models.place import Place
from models.city import City
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import jsonify, request


@app_views.route("/cities/<city_id>/places", strict_slashes=False,
                 methods=['GET', 'POST'])
def places(city_id):
    """ /cities/<city_id>/places route """
    place_list = []
    city = storage.get(City, city_id)
    if city is not None:
        places = city.places
        if request.method == 'GET':
            for place in places:
                place_list.append(place.to_dict())
            return jsonify(place_list)
        elif request.method == 'POST':
            try:
                new_dict = request.get_json()
                if 'user_id' not in new_dict.keys():
                    return {"error": "Missing user_id"}, 400
                if 'name' not in new_dict.keys():
                    return {"error": "Missing name"}, 400
                if storage.get(User, new_dict['user_id']) is None:
                    return {"error": "Not found"}, 404
                new_dict.update({'city_id': city_id})
                new_inst = Place(**new_dict)
                new_inst.save()
                return jsonify(new_inst.to_dict()), 201
            except:
                return {"error": "Not a JSON"}, 400
    return {"error": "Not found"}, 404


@app_views.route("/places/<place_id>", strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def place_id(place_id):
    """ /places/<place_id> route """
    ignore_list = ["id", "user_id", "city_id", "created_at", "updated_at"]
    place = storage.get(Place, place_id)
    if place is not None:
        if request.method == 'GET':
            return jsonify(place.to_dict())
        elif request.method == 'DELETE':
            storage.delete(place)
            storage.save()
            return {}, 200
        elif request.method == 'PUT':
            try:
                new_dict = request.get_json()
                place_dict = place.to_dict()
                for key, value in new_dict.items():
                    if key not in ignore_list:
                        place_dict.update({key: value})
                storage.delete(place)
                storage.new(Place(**place_dict))
                storage.save()
                return jsonify(place_dict), 200
            except:
                return {"error": "Not a JSON"}, 400
    return {"error": "Not found"}, 404
