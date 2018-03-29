class User(object):
    """docstring for ClassName"""

    def __init__(self, email=None, password=None, role=None):
        self.email = email
        self.password = password
        self.role = role
        super(User, self).__init__()


class Admin(User):

    def __init__(self, email, password, role="admin"):
        super(Admin, self).__init__()


class Student(User):

    def __init__(self, email, password, role="student"):
        super(Student, self).__init__()


class Book(object):
    def __init__(self, bookid="", book_name="", category="", available=True):
        self.bookid = bookid
        self.book_name = book_name
        self.category = category
        self.available = available
        super(Book, self).__init__()


class Borrow(Book, User):
    """Mutltiple inheritance"""

    def __init__(self, bookid="", email="", available=True):
        super(Borrow, self).__init__(bookid, email, available)


class Return(Book, User):
    """This class is for Return"""

    def __init__(self, email):
        super(Return, self).__init__()
