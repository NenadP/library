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
            self.show_library_items(self.items)
        if action == "2":
            self.show_library_users()
        if action == "5":
            self.borrow_return_book_menu()

        print ""
        print "Press enter to return to menu"
        input()
        self.show_menu()

    # Prints Library Items
    def show_library_items(self, items):
        print "Library currently has following items:"
        print ""
        for item in items:
            print "Id: {id}".format(id=item.item_id)
            print "{title} ({type}), {year}".format(title=item.title, type=item.item_type, year=item.year)
            if item.item_type == "book":
                print "Author: {author}".format(author=item.author)
                print "ISBN: {isbn}".format(isbn=item.isbn)
                print "Borrowed: {is_borrowed} ".format(is_borrowed = "Yes" if item.is_borrowed == True else "No")
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

    # Menu to trigger borrow or return action
    def borrow_return_book_menu(self):
        print "Do you want to borrow(1), or return a book(2)?"
        answer = input()
        if answer == "1":
            self.borrow_book()
        if answer == "2":
            self.return_book()

    # Borrow book from the library
    # Asks for a user to lend to, book to borrow and then sets is_borrowed on selected book to True
    # and adds a book to user.borrowed_books
    def borrow_book(self):
        print "Borrow a book for which user?"
        selected_user = self.select_by_id(self.users, "user")
        print "Which book to borrow?"
        selected_book = self.select_by_id(self.items, "book")
        if selected_book.item_type == "periodical":
            print "Sorry you can't borrow Periodical"
            print ""
            self.borrow_book()
        elif selected_book.is_borrowed is True:
            print "Sorry this book is already lend"
            print ""
            self.borrow_book()
        else:
            selected_book.is_borrowed = True
            selected_user.borrowed_books.append(selected_book)
            print "Book {book} lend to user: {name}".format(book=selected_book.title, name=selected_user.name)

    # Return book from the library
    # Asks for a user which returns a book, book to return and then sets is_borrowed on selected book to False
    # and removes a book to user.borrowed_books
    def return_book(self):
        print "Return a book for which user?"
        selected_user = self.select_by_id(self.users, "user")
        print "Which book do you want to return?"
        selected_book = self.select_by_id(selected_user.borrowed_books, "book")

        if selected_book:
            selected_book.is_borrowed = False
            selected_user.borrowed_books.remove(selected_book)
            print "Book {book} was returned by user: {name}".format(book=selected_book.title, name=selected_user.name)

    # This method takes items (could be users, library items or user borrowed items), item_id_property
    # ("user" or "book") to determine helper show methods and determine item_id when searchin inside of items
    # It returns selected_item whish is and object found based on user input
    def select_by_id(self, items, select_type_param):
        print "(Type in {select_type} ID to select one, or type \"s\" to show list {select_type}s)" \
            .format(select_type=select_type_param)
        answer = input()
        selected_item = None
        item_id_property = "user_id" if select_type_param == "user" else "item_id"
        if answer == "s":
            if select_type_param == "book":
                self.show_library_items(items)
                return self.select_by_id(items, select_type_param)
            if select_type_param == "user":
                self.show_library_users()
                return self.select_by_id(items, select_type_param)
        else:
            answer_int = int(answer)
            for item in items:
                item_id = getattr(item, item_id_property)
                if item_id == answer_int:
                    selected_item = item
                    break
            if selected_item is None:
                print "I did not find {select_type} with that ID.".format(select_type=select_type_param)
                return self.select_by_id(items, select_type_param)
        return selected_item

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