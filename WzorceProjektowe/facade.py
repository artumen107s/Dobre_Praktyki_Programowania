from singleton import LibraryCatalog

class LibraryInterface:
    def __init__(self):
        self.catalog = LibraryCatalog.get_instance()

    def search_book(self, book_id):
        return self.catalog.get_book(book_id)

    def add_book(self, book_id, book_title):
        self.catalog.add_book(book_id, book_title)
        return f"Book '{book_title}' added."
