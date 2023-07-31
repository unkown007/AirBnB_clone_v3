#!/usr/bin/python3
""" setup routes """
from api.v1.views import app_views
from flask import jsonify
from models import storage


hbnbData = {
        "amenities": "Amenity",
        "cities": "City",
        "places": "Place",
        "reviews": "Review",
        "states": "State",
        "users": "User",
        }


@app_views.route("/status", strict_slashes=False)
def status():
    """ return the status of the api """
    return jsonify({"status": "OK"})


@app_views.route("/stats", strict_slashes=False)
def stats():
    """ returns the statistics of the data """
    dict_stat = {}
    for key, value in hbnbData.items():
        dict_stat[key] = storage.count(value)
    return jsonify(dict_stat)
