import csv
import sqlite3

class Book:     
    '''Create a book class 
    '''
    def __init__(self, book_id, name, pages, author):
        self.book_id = book_id
        self.name = name
        self.pages = pages
        self.author = author

class BookInventory:    
    """
    This is a book inventory class to add, view, edit, and delete books.
    """
    
    def __init__(self):
        self.books = []  # An empty list to store all the books
        self.load_books_from_csv()

    def load_books_from_csv(self):
        try:
            with open("C:/Users/HP/Desktop/python temp/inventory.csv", 'r') as database: #Read from the csv file
                reader = csv.reader(database)
                next(reader)  # Skip the header
                for book in reader:
                    new_book = Book(int(book[0]), book[1], int(book[2]), book[3])
                    self.books.append(new_book)
        except FileNotFoundError:
            print("Inventory file not found. Starting with an empty inventory.")
            
    def add_books_to_db(self):
        mydb = sqlite3.connect('my.db')
        
        
        cursor = mydb.execute("")
        

    def save_books_to_csv(self):
        with open("C:/Users/HP/Desktop/python temp/inventory.csv", 'w', newline='') as database:
            writer = csv.writer(database)
            writer.writerow(["ID", "Name", "Pages", "Author"])
            for book in self.books:
                writer.writerow([book.book_id, book.name, book.pages, book.author])

    def add(self):
        name = input("\nEnter the name of the book:\n\t").strip()  # Strip whitespace
        if name == '':
            print("Title cannot be empty")
            return

        attempt_count = 0  # A count to allow just 3 wrong attempts
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

        book_id = len(self.books) + 1  # Incremental book ID
        new_book = Book(book_id, name, pages, author)
        self.books.append(new_book)
        print(f"You have successfully added '{name}' with ID {book_id}")
        
        self.save_books_to_csv()

    def view(self):
        if not self.books:
            print("There are no books in inventory.\n")
            return
        
        print("Books in inventory:")
        for book in self.books:
            print(f"ID: {book.book_id} | Name: {book.name} | Pages: {book.pages} | Author: {book.author}")

    def delete(self):
        attempt_count = 0
        while attempt_count < 3:
            try:
                book_id = int(input("\nEnter the ID of the book you want to remove:\n\t"))
                if 1 <= book_id <= len(self.books):
                    removed_book = self.books.pop(book_id - 1)
                    print(f"Book '{removed_book.name}' with ID {book_id} deleted.")
                    self.reassign_ids()
                    self.save_books_to_csv()
                    break
                else:
                    attempt_count += 1
                    print(f"Book with ID {book_id} not found. You have {3 - attempt_count} attempts left.")
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
                if 1 <= book_id <= len(self.books):
                    book = self.books[book_id - 1]

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
                    print(f"Book with ID {book_id} has been edited.")
                    break
                else:
                    attempt_count += 1
                    print(f"Book with ID {book_id} not found. You have {3 - attempt_count} attempts left.")
            except ValueError:
                attempt_count += 1
                print(f"Invalid input. Please enter a valid book ID. You have {3 - attempt_count} attempts left.")

        if attempt_count == 3:
            print("Too many invalid attempts. Returning to the home page.")

    def reassign_ids(self):
        for i, book in enumerate(self.books):
            book.book_id = i + 1  # Re-assigning new IDs to the books after deletion
        self.save_books_to_csv()


# Main program loop
new_inventory = BookInventory()

while True:
    print("\n\tWelcome to Bonneyxy's book inventory assistant..")
    option = input("\n\tEnter\n\n\t 1. To add a book to the inventory\n\t 2. To edit an existing book\n\t 3. To view books\n\t 4. To delete a book\n\t 5. To exit\n")
    
    if option == "1":
        new_inventory.add()

    elif option == "2":
        new_inventory.edit()

    elif option == "3":
        new_inventory.view()

    elif option == "4":
        new_inventory.delete()

    elif option == "5":
        print("Exiting the inventory assistant.")
        break

    else:
        print("Invalid option, please try again.")
