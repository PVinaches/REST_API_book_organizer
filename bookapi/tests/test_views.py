from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
import json
from ..models import Book, BookCreator, User, Library


# Initialize the API application
client = APIClient()

# Test create user view
class TestCreateUser(APITestCase):
    def setUp(self):
        # Prepare form data
        self.valid_user = {
            'username': 'test',
            'email': 'test@email.com',
            'password': 'testpassword'
        }
        self.invalid_user = {
            'username': '',
            'email': 'test@email.com',
            'password': 'testpassword'
        }

    def test_create_valid_user(self):
        response = self.client.post(
            reverse('create_user'),
            data=json.dumps(self.valid_user),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_create_invalid_user(self):
        response = self.client.post(
            reverse('create_user'),
            data=json.dumps(self.invalid_user),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

# Test get_all_books view
class TestGetAllBooks(APITestCase):
    def setUp(self):
        # Prepare user data
        User.objects.create_user(username='test', email= 'test@email.com', password='test123')
        self.user = User.objects.get(username='test')
        
        # Prepare answer
        Book.objects.create(title='Alice in Borderland', author='Haro Aso',year='2011', language='French', editorial='Delcourt', ISBN='978-2-7560-3707-3')
        Book.objects.create(title='Clean Code. A handbook of Agile software craftsmanship', author='Robert C Martin',year='2009', language='English', editorial='Pearson', ISBN='978-0-13-235088-4')
        self.expected_books = [
            {
                "title": "Alice in Borderland", 
                "author": "Haro Aso",
                "year": 2011,
                "language": "French",
                "editorial": "Delcourt", 
                "ISBN": "978-2-7560-3707-3"
            },
            {
                "title": "Clean Code. A handbook of Agile software craftsmanship", 
                "author": "Robert C Martin",
                "year": 2009,
                "language": "English",
                "editorial": "Pearson", 
                "ISBN": "978-0-13-235088-4"
            }
        ]
    
    def test_get_all_books(self):
        self.client.force_login(user=self.user)
        response = self.client.get(reverse('books'))
        self.assertEqual(response.data, JSONRenderer().render(self.expected_books))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

# Test add_book view 
class TestAddBook(APITestCase):
    def setUp(self):
        # Prepare user data
        User.objects.create_user(username='test', email= 'test@email.com', password='test123')
        self.user = User.objects.get(username='test')

        # Prepare answer
        self.valid_book = {
            'title': 'Alice in Borderland', 
            'author': 'Haro Aso',
            'year': '2011',
            'language': 'French',
            'editorial': 'Delcourt',
            'ISBN': '978-2-7560-3707-3'
        }
        self.invalid_book = {
            'title': '', 
            'author': 'Haro Aso',
            'year': '2011',
            'language': 'French',
            'editorial': 'Delcourt',
            'ISBN': '978-2-7560-3707-3'
        }
    
    def test_create_valid_book(self):
        self.client.force_login(user=self.user)
        response = self.client.post(
            reverse('books'),
            data=json.dumps(self.valid_book),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_create_invalid_book(self):
        self.client.force_login(user=self.user)
        response = self.client.post(
            reverse('books'),
            data=json.dumps(self.invalid_book),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

# Test get_book view 
class TestGetBook(APITestCase):
    def setUp(self):
        # Prepare user data
        User.objects.create_user(username='test', email= 'test@email.com', password='test123')
        User.objects.create_user(username='test2', email= 'test2@email.com', password='123test')
        self.user = User.objects.get(username='test')
        self.user2 = User.objects.get(username='test2')
        
        # Prepare form data
        Book.objects.create(title='Alice in Borderland', author='Haro Aso',year='2011', language='French', editorial='Delcourt', ISBN='978-2-7560-3707-3')
        Book.objects.create(title='Alice in Borderland 2', author='Haro Aso',year='2011', language='French', editorial='Delcourt', ISBN='978-2-7560-3707-4')
        BookCreator.objects.create(book_added='Alice in Borderland', poster='test')
        BookCreator.objects.create(book_added='Alice in Borderland 2', poster='test2')
        self.selected_book= {
            "title": "Alice in Borderland"
        }

        # Prepare answer
        self.expected_book = [
            {
                "title": "Alice in Borderland", 
                "author": "Haro Aso",
                "year": 2011,
                "language": "French",
                "editorial": "Delcourt", 
                "ISBN": "978-2-7560-3707-3"
            }
        ]

    def test_get_book_owner(self):
        self.client.force_login(user=self.user)
        response = self.client.post(
            reverse('book'),
            data=json.dumps(self.selected_book),
            content_type='application/json'
        )
        self.assertEqual(response.data, JSONRenderer().render(self.expected_book))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_book_not_owner(self):
        self.client.force_login(user=self.user2)
        response = self.client.post(
            reverse('book'),
            data=json.dumps(self.selected_book),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

# Test update_book view 
class TestUpdateBook(APITestCase):
    def setUp(self):
        # Prepare user data
        User.objects.create_user(username='test', email= 'test@email.com', password='test123')
        self.user = User.objects.get(username='test')
       
        # Prepare form data 
        Book.objects.create(title='Alice in Borderland', author='Haro Aso',year='2010', language='French', editorial='Delcourt', ISBN='978-2-7560-3707-3')
        BookCreator.objects.create(book_added='Alice in Borderland', poster='test')
        self.updated_book = {
            "title": "Alice in Borderland", 
            "author": "Haro Aso",
            "year": "2011",
            "language": "French",
            "editorial": "Delcourt",
            "ISBN": "978-2-7560-3707-3"
        }
    
    def test_update_book(self):
        self.client.force_login(user=self.user)
        response = self.client.put(
            reverse('book'),
            data=json.dumps(self.updated_book),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

# Test delete_book view 
class TestDeleteBook(APITestCase):
    def setUp(self):
        # Prepare user data
        User.objects.create_user(username='test', email= 'test@email.com', password='test123')
        self.user = User.objects.get(username='test')

        # Prepare form data
        Book.objects.create(title='Alice in Borderland', author='Haro Aso',year='2011', language='French', editorial='Delcourt', ISBN='978-2-7560-3707-3')
        BookCreator.objects.create(book_added='Alice in Borderland', poster='test')
        self.title = {"title": "Alice in Borderland"}
    
    def test_delete_book(self):
        self.client.force_login(user=self.user)
        response = self.client.delete(
            reverse('book'),
            data=json.dumps(self.title),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

# Test get_all_books_library view
class TestGetAllBooksLibrary(APITestCase):
    def setUp(self):
        # Prepare user data
        User.objects.create_user(username='test', email= 'test@email.com', password='test123')
        User.objects.create_user(username='test2', email= 'test2@email.com', password='123test')
        self.user = User.objects.get(username='test')
        
        # Prepare form data
        Library.objects.create(user_name='test', title_book='Alice in Borderland')
        Library.objects.create(user_name='test', title_book='Alice in Borderland 2')
        Library.objects.create(user_name='test2', title_book='Clean Code. A handbook of Agile software craftsmanship')

        # Prepare answer
        self.library_books = [
            {
                "user_name": "test",
                "title_book": "Alice in Borderland"
            },
            {
                "user_name": "test",
                "title_book": "Alice in Borderland 2"
            }
        ]
    
    def test_get_all_books(self):
        self.client.force_login(user=self.user)
        response = self.client.get(reverse('library'))
        self.assertEqual(response.data, JSONRenderer().render(self.library_books))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

# Test add_book_library view 
class TestAddBookLibrary(APITestCase):
    def setUp(self):
        # Prepare user data
        User.objects.create_user(username='test', email= 'test@email.com', password='test123')
        self.user = User.objects.get(username='test')

        # Prepare form data
        self.valid_book = {'title': 'Alice in Borderland'}
        self.invalid_book = {'title': ''}
    
    def test_add_valid_book_library(self):
        self.client.force_login(user=self.user)
        response = self.client.post(
            reverse('library'),
            data=json.dumps(self.valid_book),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_invalid_book_library(self):
        self.client.force_login(user=self.user)
        response = self.client.post(
            reverse('library'),
            data=json.dumps(self.invalid_book),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

# Test delete_book_library view 
class TestDeleteBookLibrary(APITestCase):
    def setUp(self):
        # Prepare user data
        User.objects.create_user(username='test', email= 'test@email.com', password='test123')
        self.user = User.objects.get(username='test')

        # Prepare form data
        Library.objects.create(user_name='test', title_book='Alice in Borderland')
        self.title = {'title': 'Alice in Borderland'}
    
    def test_delete_book_library(self):
        self.client.force_login(user=self.user)
        response = self.client.delete(
            reverse('library'),
            data=json.dumps(self.title),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)