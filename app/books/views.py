from flask import Blueprint, request, make_response, jsonify, session
from app.books.models import Book
from flask.views import MethodView

books = {}
borrowed = {}


book = Blueprint('book', __name__, url_prefix='/api/v1')


class Book(Book, MethodView):
    def get(self):
        """This method retrieves allbooks """
        if "user" in session.keys():
            all_books = []
            for key, value in books.items():
                all_books.append({
                    "bookid": key,
                    "book_name": value.book_name,
                    "category": value.category
                })
            return make_response(jsonify(all_books), 200)
        else:
            return make_response(jsonify({
                "message": "please login"
            }))

    def post(self):
        """This method add a book"""
        if "user" in session.keys():
            data = request.form.to_dict()
            bookid = data.get('bookid')
            book_name = data.get('book_name')
            category = data.get('category')

            if bookid == '':
                return make_response(jsonify(
                    {"error": "Enter Book id"}), 400)

            if book_name == '':
                return make_response(jsonify(
                    {"error": "Enter Book name"}), 400)
            if category == '':
                return make_response(jsonify(
                    {"error": "Enter Category"}), 400)

            if bookid in books.keys():
                return make_response(jsonify(
                    {'message': 'Book  already exist'}), 409)

            new_book = Book(bookid=bookid, book_name=book_name,
                            category=category)
            books[bookid] = new_book
            return make_response(jsonify(
                {"message": "Book Added successfully"
                 }), 201)
        else:
            return jsonify({
                "error": "please login"})


class GetBook(Book, MethodView):
    def get(self, bookid):
        """ This method gets a single book"""
        if "user" in session.keys():
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
        else:
            return make_response(jsonify({
                "error": "please login"}))


class EditBook(Book, MethodView):
    def put(self, bookid):
        """ This Method edits book"""
        if "user" in session.keys():
            if bookid in books.keys():
                data = request.form.to_dict()
                book_name = data.get('book_name')
                category = data.get('category')

                if book_name == '':
                    return make_response(jsonify(
                        {"error": "Enter Book name"}), 400)
                if category == '':
                    return make_response(jsonify(
                        {"error": "Enter Category"}), 400)

                edit_book = Book(bookid=bookid, book_name=book_name,
                                 category=category)
                books[bookid] = edit_book
                print(books)
                return make_response(jsonify(
                    {"message": "Edit successfully"
                     }), 201)
            else:
                return make_response(jsonify("No book with that id"), 404)
        else:
            return make_response(jsonify("please login"), 400)


class DeleteBook(MethodView):
    def delete(self, bookid):
        """This method delete book"""
        if "user" in session.keys():
            if bookid in books.keys():
                del books[bookid]
                return make_response(jsonify({
                    "message": "delete successful"}), 204)
            else:
                return make_response(jsonify({
                    "error": "Book does not exist."}), 404)
        else:
            return make_response(jsonify({"message": "please login"}))


class BorrowBook(MethodView):
    def post(self, bookid):
        if 'user' in session.keys():
            if bookid in books.keys():

                for bookid, value in books.items():
                    print(bookid)
                    if value.available is True:
                        borrowed[bookid] = session['user']
                        value.available = False
                        print(borrowed)

                        return jsonify('You have borrowed a book with id {}'
                                       .format(bookid))
                    else:
                        return make_response(jsonify(
                            "the book is not available"), 404)

            else:
                return make_response(jsonify("No book with that id"))
        else:
            return make_response(jsonify("please login"))


book.add_url_rule(
    '/books', view_func=Book.as_view(
        'books'), methods=['GET', 'POST'])
book.add_url_rule(
    '/books/<bookid>', view_func=GetBook.as_view(
        'getbook'), methods=['GET'])
book.add_url_rule(
    '/books/<bookid>', view_func=EditBook.as_view(
        'editbook'), methods=['PUT'])
book.add_url_rule(
    '/books/<bookid>', view_func=DeleteBook.as_view(
        'deletebook'), methods=['DELETE'])
book.add_url_rule(
    '/users/books/<bookid>', view_func=BorrowBook.as_view(
        'borrowbook'), methods=['POST'])
