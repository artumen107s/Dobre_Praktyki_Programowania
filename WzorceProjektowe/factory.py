class User:
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name

class Student(User):
    def permissions(self):
        return "Can borrow 4 books."

class Teacher(User):
    def permissions(self):
        return "Can borrow 7 books."

class Librarian(User):
    def permissions(self):
        return "UNLIMITED UNLIMITED"

class UserFactory:
    @staticmethod
    def create_user(user_type, user_id, name):
        if user_type == "student":
            return Student(user_id, name)
        elif user_type == "teacher":
            return Teacher(user_id, name)
        elif user_type == "librarian":
            return Librarian(user_id, name)
        else:
            raise ValueError("Unknown user")
