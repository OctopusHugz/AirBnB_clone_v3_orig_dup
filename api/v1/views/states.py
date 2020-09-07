#!/usr/bin/python3
""" states routes """
from models.state import State
from models import storage
from api.v1.views import app_views
from flask import jsonify, request


@app_views.route("/states", strict_slashes=False, methods=['GET', 'POST'])
def states():
    """ returns the states """
    states_list = []
    if request.method == 'GET':
        states = storage.all(State).values()
        for state in states:
            states_list.append(state.to_dict())
        return jsonify(states_list)
    elif request.method == 'POST':
        try:
            new_dict = request.get_json()
            if 'name' not in new_dict.keys():
                return {"error": "Missing name"}, 400
            new_inst = State(**new_dict)
            return jsonify(new_inst.to_dict()), 201
        except:
            return {"error": "Not a JSON"}, 400


@app_views.route("/states/<state_id>", strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def state_id(state_id):
    """ returns the state or 404 """
    states = storage.all(State).values()
    for state in states:
        if state.id == state_id:
            if request.method == 'GET':
                return jsonify(state.to_dict())
            elif request.method == 'DELETE':
                storage.delete(state)
                storage.save()
                return {}, 200
            elif request.method == 'PUT':
                try:
                    new_dict = request.get_json()
                    state_dict = state.to_dict()
                    for key, value in new_dict.items():
                        if key not in ["id", "created_at", "updated_at"]:
                            state_dict.update({key: value})
                    storage.delete(state)
                    storage.new(State(**state_dict))
                    storage.save()
                    return jsonify(state_dict), 200
                except:
                    return {"error": "Not a JSON"}, 400
    return {"error": "Not found"}, 404
