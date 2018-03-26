class User(object):
    """docstring for ClassName"""

    def __init__(self, email=None, password=None, role=None):
        self.email = email
        self.password = password
        self.role = role


class Admin(User):

    def __init__(self, email, password, role="admin"):
        super(Admin, self).__init__()


class Student(User):

    def __init__(self, email, password, role="student"):
        super(Student, self).__init__()


class Book(object):
    def __init__(self, bookid="", book_name="", category=""):
        self.bookid = bookid
        self.book_name = book_name
        self.category = category


class Borrow(Book, User):
    """Mutltiple inheritance"""

    def __init__(self, bookid, email):
        super(Borrow, self).__init__()


class Return(Book, User):
    """docstring for Return"""

    def __init__(self, email):
        super(Return, self).__init__()
