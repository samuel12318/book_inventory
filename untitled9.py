import csv
import sqlite3
import requests

class Book:
    def __init__(self, book_id, name, pages, author):
        self.book_id = book_id
        self.name = name
        self.pages = pages
        self.author = author
        self.url = "http://192.168.126.64:8080"


class BookInventory:
    def __init__(self):
        self.books = []
        self.database_path = 'my.db'
        self.load_books_from_db()
        self.url = "http://192.168.126.64:8080"

    def load_books_from_csv(self):
        try:
            with open("C:/Users/HP/Desktop/python temp/inventory.csv", 'r') as database:
                reader = csv.reader(database)
                next(reader)
                for book in reader:
                    new_book = Book(int(book[0]), book[1], int(book[2]), book[3])
                    self.books.append(new_book)
        except FileNotFoundError:
            print("Inventory file not found. Starting with an empty inventory.")

    def add_books_to_db(self):
        with sqlite3.connect(self.database_path) as connection:
            cursor = connection.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS books (
                                id INTEGER PRIMARY KEY,
                                name TEXT NOT NULL,
                                pages INTEGER NOT NULL,
                                author TEXT NOT NULL)''')
            
            for book in self.books:
                cursor.execute('''INSERT OR REPLACE INTO books (id, name, pages, author) 
                                  VALUES (?, ?, ?, ?)''', 
                               (book.book_id, book.name, book.pages, book.author))
            connection.commit()
    
    def load_books_from_db(self):
        try:
            with sqlite3.connect(self.database_path) as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM books")
                rows = cursor.fetchall()
                self.books = [Book(book_id=row[0], name=row[1], pages=row[2], author=row[3]) for row in rows]
                
        except sqlite3.Error as e:
            print("Error loading books from database:", e)
            
    def edit_books_in_db(self, book_id, new_name=None, new_pages=None, new_author=None):
        with sqlite3.connect(self.database_path) as connection:  
            cursor = connection.cursor() 
            cursor.execute('''UPDATE books 
                              SET name = COALESCE(?, name),
                                  pages = COALESCE(?, pages),
                                  author = COALESCE(?, author)
                              WHERE id = ?''', 
                           (new_name, new_pages, new_author, book_id))
            connection.commit()
        
    def delete_books_in_db(self, book_id): 
        with sqlite3.connect(self.database_path) as connection:  
            cursor = connection.cursor()  
            cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
            connection.commit()
        
    def save_books_to_csv(self):
        with open("C:/Users/HP/Desktop/python temp/inventory.csv", 'w', newline='') as database:
            writer = csv.writer(database)
            writer.writerow(["ID", "Name", "Pages", "Author"])
            for book in self.books:
                writer.writerow([book.book_id, book.name, book.pages, book.author])

    def add(self):
        name = input("\nEnter the name of the book:\n\t").strip()
        if name == '':
            print("Title cannot be empty")
            return

        attempt_count = 0
        while attempt_count < 3:
            try:
                pages = int(input("\nEnter the number of book pages (must be a number greater than 1):\n\t"))
                if pages > 1:
                    break
                else:
                    attempt_count += 1
                    print(f"Number of pages must be greater than 1. You have {3 - attempt_count} attempts left.")
            except ValueError:
                attempt_count += 1
                print(f"Invalid input. Please enter a valid number. You have {3 - attempt_count} attempts left.")

        if attempt_count == 3:
            print("Too many invalid attempts. Returning to the home page.")
            return

        author = input("\nEnter the name of the Author:\n\t").strip()
        if not author.replace(" ", "").isalpha():
            print("Invalid Author's Name")
            return

        # Calculate new book ID based on the last entry in the database
        book_id = max([book.book_id for book in self.books], default=0) + 1
        new_book = Book(book_id, name, pages, author)
        self.books.append(new_book)
        print(f"You have successfully added '{name}' with ID {book_id}")
        
        self.save_books_to_csv()
        self.add_books_to_db()
        self.add_to_Peter(book_id)

    def view(self):
        if not self.books:
            print("There are no books in inventory.\n")
            return
        
        print("Books in inventory:")
        books = self.load_from_Peter()
        if books:
            for book in books:
                print(f"ID: {book['id']} | Name: {book['title']} | Pages: {book['num_of_pages']} | Author: {book['author']}")
        else:
            print("There are no books in the inventory")

    def delete(self):
        attempt_count = 0
        while attempt_count < 3:
            try:
                book_id = int(input("\nEnter the ID of the book you want to remove:\n\t"))
                if self.delete_in_Peter(book_id):
                    print("Deleted Successfully\n\n")
                    return
                else:
                    print("Could not delete because book does not exist")
                    return
            except ValueError:
                attempt_count += 1
                print(f"Invalid input. Please enter a valid book ID. You have {3 - attempt_count} attempts left.")

        if attempt_count == 3:
            print("Too many invalid attempts. Returning to the home page.")
        
    def edit(self):
        attempt_count = 0
        while attempt_count < 3:
            try:
                book_id = int(input("\nEnter the ID of the book you would like to edit:\n\t"))
                book = next((book for book in self.books if book.book_id == book_id), None)
                if not book:
                    attempt_count += 1
                    print(f"Book with ID {book_id} not found. You have {3 - attempt_count} attempts left.")
                    continue

                new_name = input("\nEnter the new name of the book (or press Enter to skip):\n\t").strip()
                if new_name:
                    book.name = new_name

                page_attempts = 0
                while page_attempts < 3:
                    new_pages = input("\nEnter the new number of book pages (or press Enter to skip):\n\t").strip()
                    if new_pages:
                        try:
                            new_pages = int(new_pages)
                            if new_pages > 1:
                                book.pages = new_pages
                                break
                            else:
                                page_attempts += 1
                                print(f"Number of pages must be greater than 1. You have {3 - page_attempts} attempts left.")
                        except ValueError:
                            page_attempts += 1
                            print(f"Invalid input. Please enter a valid number. You have {3 - page_attempts} attempts left.")
                    else:
                        break

                new_author = input("\nEnter the new name of the Author (or press Enter to skip):\n\t").strip()
                if new_author and new_author.replace(" ", "").isalpha():
                    book.author = new_author
                elif new_author and not new_author.replace(" ", "").isalpha():
                    print("Invalid Author's Name")
                    return
                
                self.save_books_to_csv()
                self.edit_books_in_db(book_id, new_name or None, new_pages if 'new_pages' in locals() else None, new_author or None)
                self.edit_in_Peter()
