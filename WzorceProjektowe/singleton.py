class LibraryCatalog:
    _instance = None

    def __init__(self):
        if LibraryCatalog._instance is not None:
            raise Exception("Singleton must be something")
        self.books = {}
        LibraryCatalog._instance = self

    @staticmethod
    def get_instance():
        if LibraryCatalog._instance is None:
            LibraryCatalog()
        return LibraryCatalog._instance

    def add_book(self, book_id, book_title):
        self.books[book_id] = book_title

    def get_book(self, book_id):
        return self.books.get(book_id, "Book not found")
