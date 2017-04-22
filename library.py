import itertools
import datetime

input = raw_input

class Library:
    def __init__(self):
        self.items = []
        self.users = []
        self.get_default_books()
        self.get_default_users()

    # Show main menu
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
        if action == "3":
            self.search_items()
        if action == "4":
            self.search_users()
        if action == "5":
            self.borrow_return_book_menu()
        if action == "6":
            self.add_remove_item()

        print ""
        print "Press enter to return to menu"
        input()
        self.show_menu()

    # Prints Library Items
    def show_library_items(self, items):
        print "Library currently has following items:"
        print ""
        for item in items:
            item.show()

    # Print Library Users
    def show_library_users(self):
        print "Library currently has following users:"
        print ""
        for user in self.users:
            user.show()

    # Search for books and periodicals by chosen option
    def search_items(self):
        print "Search book or periodicals"
        search_parameters = ["item_id", "title", "author", "isbn", "year", "item_type", "editor", "volume", "issue"]
        self.search(search_parameters, self.items)

    # Search for users by chosen option
    def search_users(self):
        print "Search for users"
        search_parameters = ["user_id", "name", "address"]
        self.search(search_parameters, self.users)

    # Search for users, books or periodicals
    # Menu will ask to choose from search_parameter provided, and then for actual search string
    # The record and a search string provided will be converted to string and made lowercase
    # it will search in items, and print out results if found, if not it will inform
    # user that search did not yield any results
    def search(self, search_parameters, items):
        print "Enter search parameter:"
        search_parameters_string = ""

        for index, param in enumerate(search_parameters):
            search_parameters_string += "({option}){param}".format(option=index + 1, param=param)
            if index != len(search_parameters) - 1:
                search_parameters_string += ", "
        print search_parameters_string
        answer = input()

        prop = int(answer)
        if 0 < prop < 10:
            search_parameter = search_parameters[prop - 1]
            print "You are searching by: {search_parameter}".format(search_parameter=search_parameter)
            print "Enter search string:"
            search_string = input()
            search_string = search_string.lower()
            items_found = []

            for item in items:
                value = getattr(item, search_parameter, None)
                value = str(value)
                value = value.lower()
                is_found = value.find(search_string) > -1

                if is_found:
                    items_found.append(item)

            if len(items_found) > 0:
                for item in items_found:
                    item.show()
            else:
                print "Your search didn't yield any results"
        else:
            print "Sorry, you didn't chose valid available option."
            print ""
            return self.search_items()

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

    def add_remove_item(self):
        print "Do you want to (1)add or (2)remove a book from Library?"
        answer = input()
        if answer == "1":
            self.add_book()
        elif answer == "2":
            self.remove_item()
        else:
            print "Invalid option selected"
            print ""
            return  self.add_book()

    # Adds library item to library
    def add_book(self):
        print ("Adding Lybrary item")
        title = input("Enter book title:")
        author = input("Enter book author:")
        isbn = Book.input_isbn()
        year = Book.input_year()

        new_book = Book(isbn, title, author, year)
        self.items.append(new_book)
        print "Book added to Library under id: {id}".format(id=new_book.item_id)

    # Removes library item from library
    def remove_item(self):
        print ("Please enter ID of book or periodical to remove:")
        is_found = False
        book_id = input()
        for item in self.items:
            print (item.item_id, int(book_id))
            if item.item_id == int(book_id):
                is_found = True
                print "Are you sure you want to remove: {title} (type: yes)".format(title=item.title)
                answer = input()
                if answer == "yes":
                    self.items.remove(item)
                    print "Successfully removed {type}.".format(type=item.item_type)
                    break
                else:
                    print "Cancelled removed book."
                    break
        if is_found is False:
            print "I did not find book with that id"

    # Adds user to the library
    def add_user(self):
        print("Adding new User")

    # Removes an user from the library by user_id
    def remove_user(self, user_id):
        print("Removing user with id:", user_id)

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

    # Asks user to input ISBN, validates if ISBN is an integer and contains exactly 13 numbers
    @staticmethod
    def input_isbn():
        isbn = input("Enter book ISBN:")
        isbn_len = 13
        try:
            isbn_int = int(isbn)
            is_isbn_len = len(isbn) == isbn_len
            if is_isbn_len:
                return isbn
            else:
                print "ISBN needs to be 13 numbers"
                return Book.input_isbn()
        except:
            print "ISBN must be a number"
            return  Book.input_isbn()

    # Asks user to input a year, validates if it is a number and if it is not in the future
    @staticmethod
    def input_year():
        year = input("Enter year of publishing")
        try:
            year_int = int(year)
            now = datetime.datetime.now()
            print now.year
            if year_int < now.year:
                return year
            else:
                print "Year should not be in future"
                return Book.input_year()
        except:
            print "Year must be a number"
            return Book.input_year()

    # Prints the info about Book
    def show(self):
        print "Id: {id}".format(id=self.item_id)
        print "{title} ({type}), {year}".format(title=self.title, type=self.item_type, year=self.year)
        print "Author: {author}".format(author=self.author)
        print "ISBN: {isbn}".format(isbn=self.isbn)
        print "Borrowed: {is_borrowed} ".format(is_borrowed="Yes" if self.is_borrowed == True else "No")
        print ""


# Library Item: Periodical
class Periodical(Library_item):
    def __init__(self, title, editor, year, volume, issue):
        Library_item.__init__(self, title, year, "periodical")
        self.editor = editor
        self.volume = volume
        self.issue = issue
        self.can_borrow = False

    # Prints the info about Periodical
    def show(self):
        print "Id: {id}".format(id=self.item_id)
        print "{title} ({type}), {year}".format(title=self.title, type=self.item_type, year=self.year)
        print "Editor: {editor}".format(editor=self.editor)
        print "Volume: {volume}".format(volume=self.volume)
        print "Issue: {issue}".format(issue=self.issue)
        print ""


# Library User
class User:
    get_user_id = itertools.count().next

    def __init__(self, name, address):
        self.user_id = User.get_user_id()
        self.name = name
        self.address = address
        self.borrowed_books = []

    # Prints the info about User
    def show(self):
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