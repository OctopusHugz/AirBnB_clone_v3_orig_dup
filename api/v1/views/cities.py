#!/usr/bin/python3
""" cities routes """
from models.state import State
from models.city import City
from models import storage
from api.v1.views import app_views
from flask import jsonify, request


@app_views.route("/states/<state_id>/cities", strict_slashes=False,
                 methods=['GET', 'POST'])
def cities(state_id):
    """ /states/<state_id>/cities route """
    cities_list = []
    state = storage.get(State, state_id)
    if state is not None:
        cities = state.cities
        if request.method == 'GET':
            for city in cities:
                cities_list.append(city.to_dict())
            return jsonify(cities_list)
        elif request.method == 'POST':
            try:
                new_dict = request.get_json()
                if 'name' not in new_dict.keys():
                    return {"error": "Missing name"}, 400
                new_dict.update({'state_id': state_id})
                new_inst = City(**new_dict)
                new_inst.save()
                return jsonify(new_inst.to_dict()), 201
            except:
                return {"error": "Not a JSON"}, 400
    return {"error": "Not found"}, 404


@app_views.route("/cities/<city_id>", strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def city_id(city_id):
    """ returns the city or 404 """
    city = storage.get(City, city_id)
    if city is not None:
        if request.method == 'GET':
            return jsonify(city.to_dict())
        elif request.method == 'DELETE':
            storage.delete(city)
            storage.save()
            return {}, 200
        elif request.method == 'PUT':
            try:
                new_dict = request.get_json()
                city_dict = city.to_dict()
                for key, value in new_dict.items():
                    if key not in ["id", "created_at", "updated_at"]:
                        city_dict.update({key: value})
                storage.delete(city)
                storage.new(City(**city_dict))
                storage.save()
                return jsonify(city_dict), 200
            except:
                return {"error": "Not a JSON"}, 400
    return {"error": "Not found"}, 404
