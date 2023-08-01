#!/usr/bin/python3
""" handles default RESTFull API actions """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def get_amenities():
    """ Retrieves the list of all Amenity """
    amenities = storage.all("Amenity").values()
    new_amenities = []
    for amenity in amenities:
        new_amenities.append(amenity.to_dict())
    return jsonify(new_amenities)


@app_views.route(
        "/amenities/<amenity_id>", methods=["GET"], strict_slashes=False)
def get_amenity(amenity_id):
    """ Retrieve a Amenity
    Args:
        amenity_id(str): Amenity object id
    Return: JSON object with Amenity object as element
    """
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route(
        "/amenities/<amenity_id>", methods=["DELETE"], strict_slashes=False)
def delete_amenity(amenity_id):
    """ Deletes a Amenity
    Args:
        amenity_id(str): Amenity object id
    Return: empty JSON object, or 404
    """
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    amenity.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def create_amenity():
    """ Creates a new amenity """
    data = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    if "name" not in data:
        return jsonify({"error": "Missing name"}), 400
    amenity = Amenity(**data)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route(
        "/amenities/<amenity_id>", methods=["PUT"], strict_slashes=False)
def update_amenity(amenity_id):
    """ update Amenity """
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    data = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict()), 200