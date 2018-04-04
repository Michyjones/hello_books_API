import os
from flask import Flask
from app.users.views import user
from app.books.views import book


flask_app = Flask(__name__)
flask_app.secret_key = os.urandom(24)


flask_app.register_blueprint(user)
flask_app.register_blueprint(book)
