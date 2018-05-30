import os
from flask import Flask, jsonify, request
from app.users.views import user
from app.books.views import book


flask_app = Flask(__name__)
flask_app.secret_key = os.urandom(24)


flask_app.register_blueprint(user)
flask_app.register_blueprint(book)


@flask_app.errorhandler(404)
def invalidendpoints(error=None):
    """Method for invalid endpoints."""
    message = {
        'message': 'The url entered is Invalid!!!',
        'URL': 'Not found : ' + request.url
    }
    return jsonify(message), 404


@flask_app.errorhandler(405)
def notallowed(error=None):
    """Method for not allowed endpoints."""
    message = {
        'message': 'You are not Allowed to use the Method!!!',
        'URL': 'Not Allowed : ' + request.url}
    return jsonify(message), 405


@flask_app.errorhandler(400)
def Badrequest(error=None):
    """Method for not allowed endpoints."""
    message = {
        "Error": "Bad request. Enter data in JSON format"}
    return jsonify(message), 400
