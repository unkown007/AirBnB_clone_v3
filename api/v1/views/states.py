#!/usr/bin/python3
""" handles default RESTFull API actions """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def get_states():
    """ Return all states """
    states = storage.all("State").values()
    new_states = []
    for state in states:
        new_states.append(state.to_dict())
    return jsonify(new_states)


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def get_state(state_id):
    """ retrieves the State Object(s)
    state_id(str): object id
    Return: json object or raise 404 error
    """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route(
        "/states/<state_id>", methods=["DELETE"], strict_slashes=False)
def del_state(state_id):
    """ Delete a State
    state_id(str): object id
    Return: empty json, or raise 404
    """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({})


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create_state():
    """ Create a new state """
    data = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    if "name" not in data:
        return jsonify({"error": "Missing name"}), 400
    state = State(**data)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route(
        "/states/<state_id>", methods=["PUT"], strict_slashes=False)
def update_state(state_id):
    """ updates a State object
    Args:
        state_id(str): object id
    Return:"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    data = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
