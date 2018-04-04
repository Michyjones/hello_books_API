class Book(object):
    def __init__(self, bookid="", book_name="", category="", available=True):
        self.bookid = bookid
        self.book_name = book_name
        self.category = category
        self.available = available

    