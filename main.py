import json
import os

DATA_FILE = "library_data.json"


# -------------------- BOOK CLASSES --------------------
class Book:
    def __init__(self, book_id, title, author):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.is_borrowed = False
        self.type = "General"

    def to_dict(self):
        return self.__dict__


class ReferenceBook(Book):
    def __init__(self, book_id, title, author):
        super().__init__(book_id, title, author)
        self.type = "Reference"


# -------------------- USER CLASS --------------------
class User:
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name
        self.borrowed_books = []

    def to_dict(self):
        return self.__dict__


# -------------------- LIBRARY CLASS --------------------
class Library:
    def __init__(self):
        self.books = {}
        self.users = {}
        self.load_data()

    # ---------- FILE HANDLING ----------
    def save_data(self):
        data = {
            "books": {bid: book.to_dict() for bid, book in self.books.items()},
            "users": {uid: user.to_dict() for uid, user in self.users.items()}
        }
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)

    def load_data(self):
        if not os.path.exists(DATA_FILE):
            return

        with open(DATA_FILE, "r") as f:
            data = json.load(f)

        for bid, b in data.get("books", {}).items():
            if b["type"] == "Reference":
                book = ReferenceBook(b["book_id"], b["title"], b["author"])
            else:
                book = Book(b["book_id"], b["title"], b["author"])
            book.is_borrowed = b["is_borrowed"]
            self.books[bid] = book

        for uid, u in data.get("users", {}).items():
            user = User(u["user_id"], u["name"])
            user.borrowed_books = u["borrowed_books"]
            self.users[uid] = user

    # ---------- BOOK OPERATIONS ----------
    def add_book(self):
        book_id = input("Book ID: ")
        title = input("Title: ")
        author = input("Author: ")
        book_type = input("Type (general/reference): ").lower()

        if book_type == "reference":
            book = ReferenceBook(book_id, title, author)
        else:
            book = Book(book_id, title, author)

        self.books[book_id] = book
        self.save_data()
        print("Book added successfully.")

    def view_books(self):
        if not self.books:
            print("No books available.")
            return

        for book in self.books.values():
            status = "Borrowed" if book.is_borrowed else "Available"
            print(f"{book.book_id} | {book.title} | {book.author} | {book.type} | {status}")

    def search_book(self):
        keyword = input("Enter title or author to search: ").lower()
        found = False
        for book in self.books.values():
            if keyword in book.title.lower() or keyword in book.author.lower():
                print(f"{book.book_id} | {book.title} | {book.author}")
                found = True
        if not found:
            print("No matching books found.")

    # ---------- USER OPERATIONS ----------
    def add_user(self):
        user_id = input("User ID: ")
        name = input("User Name: ")
        self.users[user_id] = User(user_id, name)
        self.save_data()
        print("User added successfully.")

    # ---------- BORROW / RETURN ----------
    def borrow_book(self):
        user_id = input("User ID: ")
        book_id = input("Book ID: ")

        if user_id not in self.users or book_id not in self.books:
            print("Invalid user or book ID.")
            return

        book = self.books[book_id]

        if book.type == "Reference":
            print("Reference books cannot be borrowed.")
            return

        if book.is_borrowed:
            print("Book already borrowed.")
            return

        book.is_borrowed = True
        self.users[user_id].borrowed_books.append(book_id)
        self.save_data()
        print("Book borrowed successfully.")

    def return_book(self):
        user_id = input("User ID: ")
        book_id = input("Book ID: ")

        if user_id in self.users and book_id in self.users[user_id].borrowed_books:
            self.users[user_id].borrowed_books.remove(book_id)
            self.books[book_id].is_borrowed = False
            self.save_data()
            print("Book returned successfully.")
        else:
            print("Return failed.")


# -------------------- MAIN MENU --------------------
def main():
    library = Library()

    while True:
        print("\n--- Library Management System ---")
        print("1. Add Book")
        print("2. View Books")
        print("3. Search Book")
        print("4. Add User")
        print("5. Borrow Book")
        print("6. Return Book")
        print("7. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            library.add_book()
        elif choice == "2":
            library.view_books()
        elif choice == "3":
            library.search_book()
        elif choice == "4":
            library.add_user()
        elif choice == "5":
            library.borrow_book()
        elif choice == "6":
            library.return_book()
        elif choice == "7":
            print("Exiting system...")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
