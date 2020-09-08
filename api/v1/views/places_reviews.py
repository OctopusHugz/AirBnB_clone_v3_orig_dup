#!/usr/bin/python3
""" places routes """
from models.place import Place
from models.review import Review
from models.city import City
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import jsonify, request


@app_views.route("/places/<place_id>/reviews", strict_slashes=False,
                 methods=['GET', 'POST'])
def reviews(place_id):
    """ /places/<place_id>/reviews route """
    review_list = []
    place = storage.get(Place, place_id)
    if place is not None:
        reviews = place.reviews
        if request.method == 'GET':
            for review in reviews:
                review_list.append(review.to_dict())
            return jsonify(review_list)
        elif request.method == 'POST':
            try:
                new_dict = request.get_json()
                if 'user_id' not in new_dict.keys():
                    return {"error": "Missing user_id"}, 400
                if 'text' not in new_dict.keys():
                    return {"error": "Missing text"}, 400
                if storage.get(User, new_dict['user_id']) is None or
                storage.get(Place, new_dict['place_id']) is None:
                    return {"error": "Not found"}, 404
                new_inst = Review(**new_dict)
                new_inst.save()
                return jsonify(new_inst.to_dict()), 201
            except:
                return {"error": "Not a JSON"}, 400
    return {"error": "Not found"}, 404


@app_views.route("/reviews/<review_id>", strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def review_id(review_id):
    """ /reviews/<review_id> route """
    ignore_list = ["id", "user_id", "city_id", "created_at", "updated_at"]
    review = storage.get(Review, review_id)
    if review is not None:
        if request.method == 'GET':
            return jsonify(review.to_dict())
        elif request.method == 'DELETE':
            storage.delete(review)
            storage.save()
            return {}, 200
        elif request.method == 'PUT':
            try:
                new_dict = request.get_json()
                review_dict = review.to_dict()
                for key, value in new_dict.items():
                    if key not in ignore_list:
                        review_dict.update({key: value})
                storage.delete(review)
                storage.new(Review(**review_dict))
                storage.save()
                return jsonify(review_dict), 200
            except:
                return {"error": "Not a JSON"}, 400
    return {"error": "Not found"}, 404
