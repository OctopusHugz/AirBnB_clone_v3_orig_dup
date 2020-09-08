#!/usr/bin/python3
""" User routes """
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import jsonify, request


@app_views.route("/users", strict_slashes=False,
                 methods=['GET', 'POST'])
def users():
    """ /users route """
    user_list = []
    if request.method == 'GET':
        userz = storage.all(User).values()
        for user in userz:
            user_list.append(user.to_dict())
        return jsonify(user_list)
    elif request.method == 'POST':
        try:
            new_dict = request.get_json()
            if 'email' not in new_dict.keys():
                return {"error": "Missing email"}, 400
            if 'password' not in new_dict.keys():
                return {"error": "Missing password"}, 400
            new_inst = User(**new_dict)
            new_inst.save()
            return jsonify(new_inst.to_dict()), 201
        except:
            return {"error": "Not a JSON"}, 400
    return {"error": "Not found"}, 404


@app_views.route("/users/<user_id>", strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def user_id(user_id):
    """ returns the user or 404 """
    user = storage.get(User, user_id)
    if user is not None:
        if request.method == 'GET':
            return jsonify(user.to_dict())
        elif request.method == 'DELETE':
            storage.delete(user)
            storage.save()
            return {}, 200
        elif request.method == 'PUT':
            try:
                new_dict = request.get_json()
                user_dict = user.to_dict()
                for key, value in new_dict.items():
                    if key not in ["id", "created_at", "updated_at"]:
                        user_dict.update({key: value})
                storage.delete(user)
                storage.new(User(**user_dict))
                storage.save()
                return jsonify(user_dict), 200
            except:
                return {"error": "Not a JSON"}, 400
    return {"error": "Not found"}, 404
