import json

class JSONAdapter:
    def parse(self, data):
        return json.loads(data)

class CSVAdapter:
    def parse(self, data):
        books = {}
        for line in data.splitlines():
            book_id, title = line.split(',')
            books[book_id] = title
        return books
