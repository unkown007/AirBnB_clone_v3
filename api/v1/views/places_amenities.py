#!/usr/bin/python3
""" Amenities.py """
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.amenity import Amenity
from os import getenv


@app_views.route(
        "/places/<place_id>/amenities", methods=["GET"], strict_slashes=False)
def get_place_amenities(place_id):
    """ Retrive the list of all Amenity """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    amenities = []
    if getenv("HBNB_TYPE_STORAGE", "") == "db":
        amenity_objects = place.amenities
    else:
        amenity_objects = place.amenity_ids
    for amenity in amenity_objects:
        amenities.append(amenity.to_dict())
    return jsonify(amenities)


@app_views.route(
        "/places/<place_id>/amenities/<amenity_id>",
        methods=["DELETE"],
        strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """ Deletes a Amenity object to a Place """
    place = storage.get("Place", place_id)
    amenity = storage.get("Amenity", amenity_id)
    if place is None:
        abort(404)
    if getenv("HBNB_TYPE_STORAGE", "") == "db":
        place_amenities = place.amenities
    else:
        place_amenities = place.amenity_ids
    if amenity not in place_amenities:
        abort(404)
    place_amenities.remove(amenity)
    place.save()
    return jsonify({})


@app_views.route(
        "/places/<place_id>/amenities/<amenity_id>",
        methods=["POST"],
        strict_slashes=False)
def create_place_amenity(place_id, amenity_id):
    """ Link a Amenity object to a Place """
    place = storage.get("Place", place_id)
    amenity = storage.get("Amenity", amenity_id)
    if place is None or amenity is None:
        abort(404)
    if getenv("HBNB_TYPE_STORAGE", "") == "db":
        place_amenities = place.amenities
    else:
        place_amenities = place.amenity_ids
    if amenity not in place_amenities:
        place_amenity.append(amenity)
        place.save()
        return jsonify(amenity.to_dict()), 201
    return jsonify(amenity.to_dict())
