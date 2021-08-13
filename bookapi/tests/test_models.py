from django.test import TestCase
from ..models import User, Book, BookCreator, Library

# Integration test of the user model
class UserTest(TestCase):
    def setUp(self):
        User.objects.create(username='paloma', password='pass123')

    def test_authentication(self):
        user_to_test = User.objects.get(username = 'paloma')
        self.assertIsNotNone(user_to_test)
        self.assertEqual(user_to_test.username, 'paloma')

# Integration test of the book model
class BookTest(TestCase):
    def setUp(self):
        Book.objects.create(title='Alice in Borderland', author='Haro Aso', year='2011', language='French', editorial='Delcourt', ISBN='978-2-7560-3707-3')

    def test_book_self_(self):
        book_alice = Book.objects.get(title='Alice in Borderland')
        self.assertIsNotNone(book_alice)
        self.assertEqual(book_alice.__repr__(), "Alice in Borderland, Haro Aso, 2011, French, Delcourt, 978-2-7560-3707-3")
    
# Integration test of the book creator model
class BookCreatorTest(TestCase):
    def setUp(self):
        BookCreator.objects.create(poster='paloma', book_added='Alice in Borderland')
    
    def test_bookcreator_self_(self):
        book_post_added = BookCreator.objects.get(poster='paloma')
        self.assertIsNotNone(book_post_added)
        self.assertEqual(book_post_added.__repr__(), "Alice in Borderland was added by paloma")

# Integration test of the library model
class LibraryTest(TestCase):
    def setUp(self):
        Library.objects.create(user_name='paloma', title_book='Alice in Borderland')
    
    def test_library_self_(self):
        book_added = Library.objects.get(user_name='paloma')
        self.assertIsNotNone(book_added)
        self.assertEqual(book_added.__repr__(), "Alice in Borderland was added to the library.")