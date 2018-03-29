from app import UserRegister, flask_app, UserLogin, Book, GetBook, DeleteBook, EditBook

flask_app.add_url_rule(
    '/api/v1/auth/register', view_func=UserRegister.as_view(
        'register'), methods=['GET', 'POST'])
flask_app.add_url_rule(
    '/api/v1/auth/login', view_func=UserLogin.as_view(
        'login'), methods=['GET', 'POST'])
flask_app.add_url_rule(
    '/api/v1/books', view_func=Book.as_view(
        'books'), methods=['GET', 'POST'])
flask_app.add_url_rule(
    '/api/v1/books/<bookid>', view_func=GetBook.as_view(
        'getbook'), methods=['GET'])
flask_app.add_url_rule(
    '/api/v1/books/<bookid>', view_func=EditBook.as_view(
        'editbook'), methods=['PUT'])
flask_app.add_url_rule(
    '/api/v1/books/<bookid>', view_func=DeleteBook.as_view(
        'deletebook'), methods=['DELETE'])


if __name__ == '__main__':
    flask_app.run(debug=True)
