#!/usr/bin/python3
""" handles default RESTFull API actions """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City


@app_views.route(
        "/states/<state_id>/cities", methods=["GET"], strict_slashes=False)
def get_cities(state_id):
    """ Retrieves the list of all City objects of a State
    Args:
        state_id(str): State object id
    Return: JSON object with all object or raise 404
    """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    cities = []
    for city in state.cities:
        cities.append(city.to_dict())
    return jsonify(cities)


@app_views.route("/cities/<city_id>", methods=["GET"], strict_slashes=False)
def get_city(city_id):
    """ Retrieve a City object
    Args:
        city_id(str): City object id
    Return: JSON object with City object as element or 404
    """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=["DELETE"], strict_slashes=False)
def delete_city(city_id):
    """ Deletes a City object
    Args:
        city_id(str): City object id
    Return: empty JSON response, 404 otherwise
    """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return jsonify({})


@app_views.route(
        "/states/<state_id>/cities", methods=["POST"], strict_slashes=False)
def create_city(state_id):
    """ Creates a new City
    Args:
        state_id(str): State object id
    Return: JSON object with the new City, 404 otherwise
    """
    if storage.get("State", state_id) is None:
        abort(404)
    data = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    if "name" not in data:
        return jsonify({"error": "Missing name"}), 400
    data["state_id"] = state_id
    city = City(**data)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def update_city(city_id):
    """ Update a City
    Args:
        city_id(str): City object id
    Return: JSON object with the city updated
    """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    data = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in data.items():
        if key not in ["id", "state_id", "created_at", "updated_at"]:
            setattr(city, key, value)
    city.save()
    print("Hello")
    return jsonify(city.to_dict()), 200
