import unittest



class TestBookInventory(unittest.TestCase):
  def setUp(self):
    self.inventory = BookInventory()

  def test_add_book(self):
    book_id = self.inventory.add_book("The Kid", "Abena", 208)
    book = self.inventory.view_by_id(book_id)
    self.assertEqual(book['title'], "The Kid")
    self.assertEqual(book['author'], "Abena")
    self.assertEqual(book['number_of_pages'], 208)

  def test_remove_book(self):
    book_id = self.inventory.add_book("The book", "Paul", 67)
    self.inventory.remove_book(book_id)
    with self.assertRaises(ValueError):
      self.inventory.view_by_id(book_id)

  def test_edit_book(self):
    book_id = self.inventory.add_book("Shoe", "Esi", 60)
    self.inventory.edit_book(book_id, "The Hat", "Akua", 200)
    book = self.inventory.view_by_id(book_id)
    self.assertEqual(book['title'], "The Hat")
    self.assertEqual(book['author'], "Akua")
    self.assertEqual(book['number_of_pages'], 200)

  def test_view_all(self):
    self.inventory.add_book("The red Hat", "Ama", 708)
    self.inventory.add_book("The blue Hat", "Kojo", 708)
    books = self.inventory.view_all()
    self.assertEqual(len(books), 2)

  def test_view_by_id(self):
    book_id = self.inventory.add_book("The red Hat", "Ama", 708)
    book = self.inventory.view_by_id(book_id)
    self.assertEqual(book['title'], "The red Hat")
    self.assertEqual(book['author'], "Ama")
    self.assertEqual(book['number_of_pages'], 708)

if __name__ == '__main__':
  unittest.main()