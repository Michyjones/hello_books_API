import os
from app import UserRegister, flask_app, UserLogin, Book, GetBook, DeleteBook
from app import ResetPassword, EditBook, Logout, BorrowBook


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
flask_app.add_url_rule(
    '/api/v1/auth/logout', view_func=Logout.as_view(
        'logout'), methods=['POST'])

flask_app.add_url_rule(
    '/api/v1/auth/reset-password', view_func=ResetPassword.as_view(
        'reset-password '), methods=['POST'])
flask_app.add_url_rule(
    '/api/v1/users/books/<bookid>', view_func=BorrowBook.as_view(
        'borrowbook '), methods=['POST'])


# if __name__ == '__main__':
port = int(os.environ.get('PORT', 5000))
flask_app.run(host='0.0.0.0', port=port, debug=True)
