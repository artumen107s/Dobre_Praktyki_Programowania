class Observer:
    def notify(self, message):
        raise NotImplementedError

class UserObserver(Observer):
    def __init__(self, name):
        self.name = name

    def notify(self, message):
        print(f"Notification for {self.name}: {message}")

class LibraryCatalogObservable:
    def __init__(self):
        self.observers = []

    def add_observer(self, observer):
        self.observers.append(observer)

    def notify_observers(self, message):
        for observer in self.observers:
            observer.notify(message)
