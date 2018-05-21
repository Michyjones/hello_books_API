from flask import Blueprint, request, make_response, jsonify, session
from app.users.models import User

from flask.views import MethodView


users_data = {}

user = Blueprint('user', __name__, url_prefix='/api/v1/auth')


class UserRegister(User, MethodView):

    def post(self):
        # getting a dictonary from flask request form
        data = request.form.to_dict()
        email = data.get('email')
        password = data.get('password')
        role = data.get('role')

        if email == '':
            return make_response(jsonify(
                {'error': 'Enter the email'}), 400)

        if password == '':
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
        session['user'] = email
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


class Logout(MethodView):
    def post(self):
        """This method logs out user"""
        if "user" in session.keys():
            session.pop("user")
            return make_response(jsonify("You are logged Out!"), 200)
        else:
            return make_response(jsonify("You are not logged in"), 201)


class ResetPassword(User, MethodView):
    def post(self):
        """ This Method resets password """
        data = request.form.to_dict()
        email = data.get('email')
        if email in users_data.keys():
            password = data.get('new_password')

            new_user_account = User(email=email, password=password)

            users_data[email] = new_user_account
            return make_response(jsonify("password reset successfully"), 201)

        else:
            return jsonify("User account does not exist")


user.add_url_rule(
    '/register', view_func=UserRegister.as_view(
        'register'), methods=['POST'])
user.add_url_rule(
    '/login', view_func=UserLogin.as_view(
        'login'), methods=['POST'])
user.add_url_rule(
    '/logout', view_func=Logout.as_view(
        'logout'), methods=['POST'])
user.add_url_rule(
    '/reset-password', view_func=ResetPassword.as_view(
        'reset-password'), methods=['POST'])
