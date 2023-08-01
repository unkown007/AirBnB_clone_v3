#!/usr/bin/python3
""" handles default RESTFull API actions """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.review import Review


@app_views.route(
        "/places/<place_id>/reviews", methods=["GET"], strict_slashes=False)
def get_reviews(place_id):
    """ Retrieve place reviews """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    reviews = []
    for review in place.reviews:
        reviews.append(review.to_dict())
    return jsonify(reviews)


@app_views.route("/reviews/<review_id>", methods=["GET"], strict_slashes=False)
def get_review(review_id):
    """ Retrieve a review """
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route(
        "/reviews/<review_id>", methods=["DELETE"], strict_slashes=False)
def delete_review(review_id):
    """ deletes a review """
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({})


@app_views.route(
        "/places/<place_id>/reviews", methods=["POST"], strict_slashes=False)
def create_review(place_id):
    """ creates a new review """
    if storage.get("Place", place_id) is None:
        abort(404)
    data = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    if "user_id" not in data:
        return jsonify({"error": "Missing user_id"}), 400
    if storage.get("User", data["user_id"]) is None:
        abort(404)
    if "text" not in data:
        return jsonify({"error": "Missing text"}), 400
    data["place_id"] = place_id
    review = Review(**data)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=["PUT"], strict_slashes=False)
def update_review(review_id):
    """ updates a review """
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    data = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(review, key, value)
    review.save()
    return jsonfify(state.to_dict()), 200
