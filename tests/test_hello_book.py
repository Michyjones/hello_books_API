
import unittest
import run
import json
from app import flask_app


class UserAuthentication(unittest.TestCase):

    def setUp(self):
        self.client = run.flask_app.test_client()

    def test_register_user_email_isnot_null(self):
        user = {"email": "", "password": "password",
                "role": "user"}
        response = self.client.post(
            "/api/v1/auth/register", data=user,
            content_type="application/json")
        print(response.data)
        self.assertEqual(response.status_code, 400)

    def test_register_user_password_isnot_null(self):
        user = {"email": "michyjones@gmail.com", "password": "",
                "role": "user"}
        response = self.client.post(
            "/api/v1/auth/register", data=user,
            content_type="application/json")
        print(response.data)
        self.assertEqual(response.status_code, 400)

    def test_register_user_role_can_only_be_admin_or_user(self):
        user = {"email": "admin@gmail.com", "password": "qwerty123",
                "role": "manager"}
        response = self.client.post(
            "/api/v1/auth/register", data=user,
            content_type="application/json")

        self.assertEqual(response.status_code, 400)

    def test_register_password_more_than_8_character(self):
        user = {"email": "michyjones@gmail.com", "password": "rwyeue",
                "role": "user"}
        response = self.client.post(
            "/api/v1/auth/register", data=user,
            content_type="application/json")

        self.assertEqual(response.status_code, 400)

    def test_register_user_exist(self):
        user = {"email": "michyjones@gmail.com", "password": "password",
                "role": "user"}
        self.client.post(
            "/apiv1/auth/register", data=user,
            content_type="application/json")
        response = self.client.post(
            "/api/v1/auth/register", data=user,
            content_type="application/json")

        self.assertEqual(response.status_code, 409)

    def test_register_user(self):
        user = {"email": "michyjones@gmail.com", "password": "qwerty12345",
                "role": "user"}

        response = self.client.post(
            "/api/v1/auth/register", data=user,
            content_type="application/json")

        self.assertEqual(response.status_code, 201)

    def test_login_user(self):

        user = {"email": "michyjones@gmail.com", "password": "password"}
        response = self.client.post(
            "/api/v1/auth/login", data=user,
            content_type="application/json")

        self.assertEqual(response.status_code, 200)

    def test_login_user_invalid_credentials(self):
        user = {"email": "qwerty123@gmail.com", "password": "password"}
        response = self.client.post(
            "/api/v1/auth/login", data=user,
            content_type="application/json")

        self.assertEqual(response.status_code, 401)

    def test_login_user_email_is_not_null(self):
        user = {"email": "", "password": "password",
                "role": "user"}
        response = self.client.post(
            "/api/v1/auth/login", data=user,
            content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_login_user_password_is_not_null(self):
        user = {"email": "michyjones@gmail.com", "password": "",
                "role": "user"}
        response = self.client.post(
            "/api/v1/auth/login", data=user,
            content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_admin_create_book(self):
        book = {"bookid": "004", "bookname": "Introductionto flask",
                "category": "Engineering"}
        response = self.client.post(
            "/api/v1/books", data=book,
            content_type="application/json")
        self.assertEqual(response.status_code, 201)

    def test_admin_updates_a_book(self):
        book = {"bookid": "004", "bookname": "Introductionto flask",
                "category": "Engineering"}
        response = self.client.put(
            "/api/v1/books/<bookid>", data=book,
            content_type="application/json")

        self.assertEqual(response.status_code, 201)

    def test_admin_delete_a_book(self):
        book = {"bookid": "002", "bookname":
                "Introduction to programming",
                "category": "Engineering"}
        response = self.client.delete(
            "/api/v1/books/<bookid>", data=book,
            content_type="application/json")
        self.assertEqual(response.status_code, 204)

    def test_can_get_all_books(self):
        books = {"bookid": "001", "bookname": "Introductionto bootstrap",
                 "bookid": "002", "bookname": "Introduction to programming",
                 "bookid": "003", "bookname": "Introduction to javascript",
                 "bookid": "004", "bookname": "Introduction to flask",
                 "bookid": "005", "bookname": "Web development"}
        response = self.client.get(
            "/api/v1/books", data=books,
            content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_user_can_boorow_book(self):
        book = {"bookid": "004", "bookname": "Introduction to flask"}
        response = self.client.post(
            "/api/v1/users/books/<bookId>", data=book,
            content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_user_can_get_a_book(self):
        book = {"bookid": "002", "bookname": "Introduction to programming"}
        response = self.client.get(
            "/api/v1/books/<bookid>", data=book,
            content_type="application/json")
        self.assertEqual(response.status_code, 200)
