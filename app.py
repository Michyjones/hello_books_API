import os
from flask import Flask, render_template, request, make_response, jsonify, session
from models import User, Book

from flask.views import MethodView

flask_app = Flask(__name__)

users_data = {}
books = {}

flask_app.secret_key = os.urandom(24)
# print(flask_app.secret_key)


class UserRegister(User, MethodView):
    def get(self):
        return render_template('register.html')

    def post(self):
        # getting a dictonary from flask request form
        data = request.form.to_dict()
        email = data.get('email')
        password = data.get('password')
        role = data.get('role')

        if email is None:
            return make_response(jsonify(
                {'error': 'Fill in the details'}), 400)

        if password is None:
            return make_response(jsonify(
                {
                    'error': 'Fill in the details'
                }), 400)

        if (role != 'user') and (role != 'admin'):
            return make_response(jsonify(
                {'error': 'Role can only be user or admin'}), 400)

        if len(password) < 8:

            return make_response(jsonify(
                {'message': 'password should be more than 8 character'}), 400)
        if email in users_data.keys():
            return make_response(jsonify(
                {'message': 'user already exist'}), 409)

        new_user = User(email=email, password=password, role=role)
        users_data[email] = new_user
        session['user'] = email
        return make_response(jsonify({
            "message": "user_created successfully"
        }), 201)


class UserLogin(MethodView):
    def get(self):
        return render_template('login.html')

    def post(self):
        data = request.form.to_dict()
        email = data.get('email')
        password = data.get('password')

        if email is None:
            return make_response(jsonify(
                {"error": "Email required"}), 400)

        if password is None:
            return make_response(jsonify(
                {"error": "password required"}), 400)

        if email in users_data.keys():
            user_data = users_data[email]
            if password == user_data.password:
                session['user'] = user_data.email
                if user_data.role == 'user':
                    return make_response(jsonify({
                        "message": "student login successfully"
                    }), 200)
                else:
                    return make_response(jsonify({
                        "message": "Admin logged in"
                    }), 200)
        return make_response(jsonify({
            "error": "invalid credentials"
        }), 401)


class Book(Book, MethodView):
    def get(self):
        """This method retrieves allbooks """
        if "user" in session.keys():
            all_books = []
            for key, value in books.items():
                all_books.append({
                    "book_id": key,
                    "book_name": value.book_name,
                    "category": value.category
                })
            return make_response(jsonify(all_books), 200)
        else:
            return make_response(jsonify({
                "message": "please login"
            }))

    def post(self):
        data = request.form.to_dict()
        book_id = data.get('book_id')
        book_name = data.get('book_name')
        category = data.get('category')

        if book_id is None:
            return make_response(jsonify(
                {"error": "Enter Book id"}), 400)

        if book_name is None:
            return make_response(jsonify(
                {"error": "Enter Book name"}), 400)
        if category is None:
            return make_response(jsonify(
                {"error": "Enter Category"}), 400)

        if book_id in books.keys():
            return make_response(jsonify(
                {'message': 'Book  already exist'}), 409)

        new_book = Book(book_id=book_id, book_name=book_name,
                        category=category)
        books[book_id] = new_book
        print(books)
        return make_response(jsonify(
            {"message": "Book Added successfully"
             }), 201)


class GetBook(Book, MethodView):
    """ This method gets a single book"""

    def get(self, bookid):
        if bookid in books.keys():
            one_book = []
            book = books[bookid]
            one_book.append({
                "book_id": book.book_id,
                "book_name": book.book_name,
                "category": book.category})
            return make_response(jsonify(one_book), 200)

        else:
            return make_response(jsonify({
                "error": "No book with that id"
            }))
