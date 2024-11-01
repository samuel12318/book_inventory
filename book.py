class BookInventory:
    
    def __init__(self):
        self.books = {}
        self.next_id = 1

    def add_book(self, title, author, number_of_pages):
        book_id = self.next_id
        self.books[book_id] = {
        'title': title,
        'author': author,
        'number_of_pages': number_of_pages
        }
        self.next_id += 1
        return book_id

    def remove_book(self, book_id):
        if book_id in self.books:
            del self.books[book_id]
        else:
            raise ValueError("Book not found")

    def edit_book(self, book_id, title, author, number_of_pages):
        if book_id in self.books:
            self.books[book_id] = {
            'title': title,
            'author': author,
            'number_of_pages': number_of_pages
        }
        else:
            raise ValueError("Book not found")

    def view_all(self):
        return self.books.values()

    def view_by_id(self, book_id):
        if book_id in self.books:
            return self.books[book_id]
        else:
            raise ValueError("Book not found")


#End of project
                          