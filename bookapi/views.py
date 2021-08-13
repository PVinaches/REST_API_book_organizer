from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from .models import User, Book, Library
from .serializers import BookSerializer, BookCreatorSerializer, LibrarySerializer
from .permission import IsOwner

# Create user
@api_view(['GET', 'POST'])
@authentication_classes([SessionAuthentication])
@permission_classes([])
def create_user(request):
    if request.method == 'GET':
        return Response(status=status.HTTP_200_OK)
    elif request.method == 'POST':
        user_name = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        if not user_name or not password or not email:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            for user_count in range(User.objects.all().count()):
                username_check = User.objects.all()[user_count].username
                if username_check == user_name: return Response(status=status.HTTP_400_BAD_REQUEST)
            User.objects.create_user(username=user_name, password=password, email=email)
            return Response(status=status.HTTP_201_CREATED)

# Redirect to functions related to book model: get all books and add book
@api_view(['GET', 'POST'])
def redirect_books(request):
    if request.method == 'GET':
        return get_all_books()
    elif request.method == 'POST':
        return add_book(request)

# Get all books from the database
def get_all_books():
    try:
        all_books = Book.objects.all()
    except Book.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serialized_books = BookSerializer(all_books, many=True)
    return Response(JSONRenderer().render(serialized_books.data), status=status.HTTP_200_OK)

# Add book to the database
def add_book(request):
    book_data = {
            'title': request.data.get('title'),
            'author': request.data.get('author'),
            'year': int(request.data.get('year')),
            'language': request.data.get('language'),
            'editorial': request.data.get('editorial'),
            'ISBN': request.data.get('ISBN')
        }
    creator_data = {
        'poster': request.user.username,
        'book_added': request.data.get('title')
    }
    serialized_book = BookSerializer(data=book_data)
    if serialized_book.is_valid():
        serialized_book.save()
    else:
        return Response(serialized_book.errors, status=status.HTTP_400_BAD_REQUEST)
    serialized_creator = BookCreatorSerializer(data=creator_data)
    if serialized_creator.is_valid():
        serialized_creator.save()
        return Response(status=status.HTTP_201_CREATED)
    else:   
        return Response(serialized_creator.errors, status=status.HTTP_400_BAD_REQUEST)


# Redirect to functions related to book model: get, update and delete one book
@api_view(['POST', 'PUT', 'DELETE'])
def redirect_book(request):
    permissions = IsOwner(request)
    if permissions:
        if request.method == 'POST':
            return get_book(request)
        elif request.method == 'PUT':
            return update_book(request)
        elif request.method == 'DELETE':
            return delete_book(request)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

# Get selected book from the database
def get_book(request):
    title = request.data.get('title')
    try:
        chosen_book = Book.objects.filter(title=title)
        serialized_book = BookSerializer(chosen_book, many=True)
        return Response(JSONRenderer().render(serialized_book.data), status=status.HTTP_200_OK)

    except Book.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

# Update one selected book from the database
def update_book(request):
    title = request.data.get('title')
    author = request.data.get('author')
    year = int(request.data.get('year'))
    language = request.data.get('language')
    editorial=request.data.get('editorial')
    isbn = request.data.get('ISBN')
    try:
        Book.objects.filter(title=title).update(title=title, author=author, year=year, language=language, editorial=editorial, ISBN=isbn)
        return Response(status=status.HTTP_200_OK)
    except Book.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
        
# Delete one selected book from the database
def delete_book(request):
    book = request.data.get('title')
    try:
        queryset = Book.objects.filter(title=book)
        queryset.delete()
        return Response(status=status.HTTP_200_OK)                
    except Book.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

# Redirect to functions related to library model
@api_view(['GET', 'POST', 'DELETE'])
def redirect_library(request):
    if request.method == 'GET':
        return get_all_books_library(request)
    elif request.method == 'POST':
        return add_book_library(request)
    elif request.method == 'DELETE':
        return delete_book_library(request)

# Get all books from the library database
def get_all_books_library(request):
    try:
        all_books_library = Library.objects.filter(user_name=request.user.username)
    except Library.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serialized_library_books = LibrarySerializer(all_books_library, many=True)
    return Response(JSONRenderer().render(serialized_library_books.data), status=status.HTTP_200_OK)

# Add book to library database
def add_book_library(request):
    library_data = {
            'user_name': request.user.username,
            'title_book': request.data.get('title')
        }
    serialized_library = LibrarySerializer(data=library_data)
    if serialized_library.is_valid():
        serialized_library.save()
        return Response(status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)

# Delete one selected book from the library database
def delete_book_library(request):
    try:
        title_book = request.data.get('title')
        queryset = Library.objects.filter(user_name=request.user.username, title_book=title_book)
        queryset.delete()
        return Response(status=status.HTTP_200_OK)                
    except Library.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
