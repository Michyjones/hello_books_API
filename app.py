import os
from flask import Flask, request, make_response, jsonify
from models import User, Book, Borrow

from flask.views import MethodView

flask_app = Flask(__name__)

users_data = {}
books = {}
borrowed = {}

flask_app.secret_key = os.urandom(24)
# print(flask_app.secret_key)


class UserRegister(User, MethodView):

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
            return make_response(jsonify({'error': 'Enter password'}), 400)

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
        return make_response(jsonify({
            "message": "user_created successfully"
        }), 201)


class UserLogin(MethodView):
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
        all_books = []
        for key, value in books.items():
            all_books.append({
                "bookid": key,
                "book_name": value.book_name,
                "category": value.category
            })
        return make_response(jsonify(all_books), 200)

    def post(self):
        """This method add a book"""
        data = request.form.to_dict()
        bookid = data.get('bookid')
        book_name = data.get('book_name')
        category = data.get('category')

        if bookid is None:
            return make_response(jsonify(
                {"error": "Enter Book id"}), 400)

        if book_name is None:
            return make_response(jsonify(
                {"error": "Enter Book name"}), 400)
        if category is None:
            return make_response(jsonify(
                {"error": "Enter Category"}), 400)

        if bookid in books.keys():
            return make_response(jsonify(
                {'message': 'Book  already exist'}), 409)

        new_book = Book(bookid=bookid, book_name=book_name,
                        category=category)
        books[bookid] = new_book
        return make_response(jsonify(
            {"message": "Book Added successfully"}), 201)


class GetBook(Book, MethodView):
    """ This method gets a single book"""

    def get(self, bookid):
        if bookid in books.keys():
            one_book = []
            book = books[bookid]
            one_book.append({
                "bookid": book.bookid,
                "book_name": book.book_name,
                "category": book.category})
            return make_response(jsonify(one_book), 200)

        else:
            return make_response(jsonify({
                "error": "No book with that id"
            }))


class EditBook(Book, MethodView):
    def put(self, bookid):
        """ This Method edits book"""
        if bookid in books.keys():
            data = request.form.to_dict()
            book_name = data.get('book_name')
            category = data.get('category')

            if book_name is None:
                return make_response(jsonify(
                    {"error": "Enter Book name"}), 400)
            if category is None:
                return make_response(jsonify(
                    {"error": "Enter Category"}), 400)

            delete_book = Book(bookid=bookid, book_name=book_name,
                               category=category)
            books[bookid] = delete_book
            return make_response(jsonify(
                {"message": "Edit successfully"}), 201)
        else:
                return jsonify("No book with that id")


class DeleteBook(MethodView):
    def delete(self, bookid):
        """This method delete book"""
        if bookid in books.keys():
            del books[bookid]
            return make_response(jsonify(
                {"message": "delete successful"}), 204)
        else:
            return make_response(jsonify(
                {"error": "Book does not exist."}), 404)


class Logout(MethodView):
    def post(self):
        """This method logs out user"""
        if "user" in session.keys():
            session.pop("user")
            return jsonify("You are logged Out!")
        else:
            return jsonify("You are not logged in")


class ResetPassword(User, MethodView):
    def post(self):
        """ This Method resets password """
        data = request.form.to_dict()
        email = data.get('email')
        if email in users_data.keys():
            password = data.get('new_password')

            new_user_account = User(email=email, password=password)

            users_data[email] = new_user_account
            return jsonify("password reset successfully")

        else:
            return jsonify("User account does not exist")


class BorrowBook(Borrow, MethodView):
    def post(self, bookid):
            if bookid in books.keys():

                for bookid, value in books.items():
                    if value.available is True:

                        borrow = Borrow(bookid=bookid)
                        borrowed[bookid] = borrow.email
                        value.available = False

                        return jsonify('You have borrowed a book with id {}'
                                       .format(bookid))
                    else:
                        return jsonify("the book is not available")

            else:
                return jsonify("No book with that id")

