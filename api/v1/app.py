#!/usr/bin/python3
""" setup a Flask app """
from os import getenv
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from flask_cors import CORS
app = Flask(__name__)


app.register_blueprint(app_views)
cors = CORS(app, resources={"/*": {"origins": "0.0.0.0"}})

@app.teardown_appcontext
def closeSession(error):
    """ close the current SQLAlchemy section """
    storage.close()


@app.errorhandler(404)
def handle_api_error(ex):
    """ handle 404 not found error """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    app.run(
            host=getenv("HBNB_API_HOST", "0.0.0.0"),
            port=int(getenv("HBNB_API_PORT", "5000")),
            threaded=True)
