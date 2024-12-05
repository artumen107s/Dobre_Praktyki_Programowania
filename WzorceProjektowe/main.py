from singleton import LibraryCatalog
from adapter import JSONAdapter, CSVAdapter
from factory import UserFactory
from observer import UserObserver, LibraryCatalogObservable
from facade import LibraryInterface

def main():
    # === Singleton ===
    print("=== Singleton ===")
    catalog = LibraryCatalog.get_instance()
    catalog.add_book("1", "Artur Mendela")
    catalog.add_book("2", "UEK")
    catalog.add_book("3", "Testowa3")
    print(f"Book 1: {catalog.get_book('1')}")
    print(f"Book 2: {catalog.get_book('2')}")
    print(f"Book 3: {catalog.get_book('3')}")

    # === Adapter ===
    print("\n=== Adapter ===")
    json_adapter = JSONAdapter()
    csv_adapter = CSVAdapter()
    json_data = '{"3": "Refactoring"}'

    # Adding books from json
    json_file_path = "books/books.json"
    with open(json_file_path, "r") as json_file:
        json_data = json_file.read()
    catalog.books.update(json_adapter.parse(json_data))

    # Adding books from csv
    csv_file_path = "books/books.csv"
    with open(csv_file_path, "r") as csv_file:
        csv_data = csv_file.read()
    catalog.books.update(csv_adapter.parse(csv_data))

    # Reading books
    print(f"Book 4: {catalog.get_book('3')}")
    print(f"Book 5: {catalog.get_book('4')}")
    print(f"Book 6: {catalog.get_book('5')}")
    print(f"Book 7: {catalog.get_book('6')}")
    print(f"Book 8: {catalog.get_book('7')}")
    print(f"Book 9: {catalog.get_book('8')}")

    # === Factory ===
    print("\n=== Factory ===")
    student = UserFactory.create_user("student", 1, "Artur")
    teacher = UserFactory.create_user("teacher", 2, "Tomasz")
    librarian = UserFactory.create_user("librarian", 3, "Marta")
    print(f"{student.name} permissions: {student.permissions()}")
    print(f"{teacher.name} permissions: {teacher.permissions()}")
    print(f"{librarian.name} permissions: {librarian.permissions()}")

    # === Observer ===
    print("\n=== Observer ===")
    observable_catalog = LibraryCatalogObservable()
    user_observer = UserObserver("Artur")
    observable_catalog.add_observer(user_observer)
    observable_catalog.notify_observers("You have 1 more book to borrow.")

    # === Facade ===
    print("\n=== Facade ===")
    library_interface = LibraryInterface()
    print(library_interface.search_book("1"))
    print(library_interface.add_book("10", "Facade10"))
    print(library_interface.search_book("10"))

if __name__ == "__main__":
    main()
