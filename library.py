import itertools

class Library:
    def __init__(self):
        self.items = []
        self.users = []

    # Will hold initial logic for running library
    def init(self):
        self.add_item()
        self.add_item()
        print self.items[1].item_id

    # Prints Library Items
    def print_library_items(self):
        print self.items

    # Print Library Users
    def print_users(self):
        print self.users

    # Search in library using specific search type
    def search(self, search_type):
        print search_type

    # Borrow book from the library
    def borrow(self, item_type, item_id, user_id):
        print (item_type, item_id, user_id)

    # Adds user to the library
    def add_user(self):
        print("Adding new User")

    # Removes an user from the library by user_id
    def remove_user(self, user_id):
        print("Removing user with id:", user_id)

    # Adds library item to library
    def add_item(self):
        print ("Adding Lybrary item")
        item = LibraryItem('test', '2017', 'book')
        self.items.append(item)

    # Removes library item from library
    def remove_item(self, item_type, id):
        print ("Remove Item with id:", id)


# Library Item class, holds common attributes (title, year), could be of type book, periodical
# Each instance gets unigue id
class LibraryItem:
    get_item_id = itertools.count().next

    def __init__(self, title, year, item_type):
        self.item_id = LibraryItem.get_item_id()
        self.title = title
        self.year = year
        self.item_type = item_type


# Library Item: Book
class Book(LibraryItem):
    def __init__(self, isbn, title, author, year):
        LibraryItem.__init__(self, title, year, "book")
        self.isbn = isbn
        self.author = author
        self.can_borrow = True
        self.is_borrowed = False


# Library Item: Periodical
class Periodical(LibraryItem):
    def __init__(self, title, editor, year, volume, issue):
        LibraryItem.__init__(self, title, year, "periodical")
        self.editor = editor
        self.volume = volume
        self.issue = issue
        self.can_borrow = False


# Library User
class User:
    get_item_id = itertools.count().next

    def __init__(self, name, address):
        self.item_id = User.get_item_id()
        self.name = name
        self.address = address
        self.borrowed_books = []


library = Library()
library.init()