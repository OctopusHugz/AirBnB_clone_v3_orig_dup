#!/usr/bin/python3
""" amenities routes """
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from flask import jsonify, request


@app_views.route("/amenities", strict_slashes=False,
                 methods=['GET', 'POST'])
def amenities():
    """ /amenities route """
    amen_list = []
    if request.method == 'GET':
        amenitiez = storage.all(Amenity).values()
        for amenity in amenitiez:
            amen_list.append(amenity.to_dict())
        return jsonify(amen_list)
    elif request.method == 'POST':
        try:
            new_dict = request.get_json()
            if 'name' not in new_dict.keys():
                return {"error": "Missing name"}, 400
            new_inst = Amenity(**new_dict)
            new_inst.save()
            return jsonify(new_inst.to_dict()), 201
        except:
            return {"error": "Not a JSON"}, 400
    return {"error": "Not found"}, 404


@app_views.route("/amenities/<amenity_id>", strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def amenity_id(amenity_id):
    """ returns the amenity or 404 """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is not None:
        if request.method == 'GET':
            return jsonify(amenity.to_dict())
        elif request.method == 'DELETE':
            storage.delete(amenity)
            storage.save()
            return {}, 200
        elif request.method == 'PUT':
            try:
                new_dict = request.get_json()
                amenity_dict = amenity.to_dict()
                for key, value in new_dict.items():
                    if key not in ["id", "created_at", "updated_at"]:
                        amenity_dict.update({key: value})
                storage.delete(amenity)
                storage.new(Amenity(**amenity_dict))
                storage.save()
                return jsonify(amenity_dict), 200
            except:
                return {"error": "Not a JSON"}, 400
    return {"error": "Not found"}, 404
