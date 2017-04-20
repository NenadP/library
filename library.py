import itertools
input = raw_input

class Library:
    def __init__(self):
        self.items = []
        self.users = []
        self.get_default_books()
        self.get_default_users()

    # Will hold initial logic for running library
    def show_menu(self):
        print "Welcome to the Library"
        print ""
        print "Choose:"
        print "1. Show Library Items"
        print "2. Show Library Users"
        print "3. Search for a Book"
        print "4. Search for a User"
        print "5. Borrow/Return a book"
        print "6. Add/Remove an item from the library"
        print "7. Add/Remove and user from the library"
        print ""

        action = input()

        if action == "1":
            self.show_library_items()

        if action == "2":
            self.show_library_users()

        print ""
        print "Press enter to return to menu"
        input()
        self.show_menu()

    # Prints Library Items
    def show_library_items(self):
        print "Library currently has following items:"
        print ""
        for item in self.items:
            print "Id: {id}".format(id=item.item_id)
            print "{title} ({type}), {year}".format(title=item.title, type=item.item_type, year=item.year)
            if item.item_type == "book":
                print "Author: {author}".format(author=item.author)
                print "ISBN: {isbn}".format(isbn=item.isbn)
                print "Borrowed: {is_borrowed} ".format(is_borrowed = item.is_borrowed == "Yes" if item.is_borrowed == True else "No")
            if item.item_type == "periodical":
                print "Editor: {editor}".format(editor=item.editor)
                print "Volume: {volume}".format(volume=item.volume)
                print "Issue: {issue}".format(issue=item.issue)
            print ""

    # Print Library Users
    def show_library_users(self):
        print "Library currently has following users:"
        print ""
        for user in self.users:
            user.show_user()

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
    def add_book(self):
        print ("Adding Lybrary item")
        item = Library_item('test', '2017', 'book')
        self.items.append(item)

    # Removes library item from library
    def remove_book(self, item_type, id):
        print ("Remove Item with id:", id)

    # Add few books to the Library to start with
    def get_default_books(self):
        hobbit = Book(9780048231277, "The Hobbit", "J.R.R. Tolkien", 1973)
        war_and_peace = Book(9781853260629, "War and Peace", "Leo Tolstoy", 1997)
        the_jungle_book = Book(9781620280119, "The Jungle Book", "Rudyard Kipling", 2013)
        self.items.extend([hobbit, war_and_peace, the_jungle_book])

        irish_times_1933_1 = Periodical("The Irish Times 1","John Edward Healy", 1993, 20, 1457)
        irish_times_1933_2 = Periodical("The Irish Times 2", "John Edward Healy", 1993, 20, 1458)
        self.items.extend([irish_times_1933_1, irish_times_1933_2])

    def get_default_users(self):
        natasha = User("Natasha Susnjic Pantic", "Charlesland Grove, Greystones")
        self.users.append(natasha)

# Library Item class, holds common attributes (title, year), could be of type book, periodical
# Each instance gets unigue id
class Library_item:
    get_item_id = itertools.count().next

    def __init__(self, title, year, item_type):
        self.item_id = Library_item.get_item_id()
        self.title = title
        self.year = year
        self.item_type = item_type


# Library Item: Book
class Book(Library_item):
    def __init__(self, isbn, title, author, year):
        Library_item.__init__(self, title, year, "book")
        self.isbn = isbn
        self.author = author
        self.can_borrow = True
        self.is_borrowed = False


# Library Item: Periodical
class Periodical(Library_item):
    def __init__(self, title, editor, year, volume, issue):
        Library_item.__init__(self, title, year, "periodical")
        self.editor = editor
        self.volume = volume
        self.issue = issue
        self.can_borrow = False


# Library User
class User:
    get_user_id = itertools.count().next

    def __init__(self, name, address):
        self.user_id = User.get_user_id()
        self.name = name
        self.address = address
        self.borrowed_books = []

    def show_user(self):
        print "Id: {id}".format(id=self.user_id)
        print "Name: {name}".format(name=self.name)
        print "Address: {address}".format(address=self.address)
        print "Borrowed Books:"
        self.show_user_borrowed_books_excerpt()
        print ""

    def show_user_borrowed_books_excerpt(self):
        if len(self.borrowed_books) == 0:
            print "No books borrowed."
        else:
            for book in self.borrowed_books:
                print "Id: {id}, {title},{author}".format(id=book.item_id, title=book.title, author=book.author)

library = Library()
library.show_menu()