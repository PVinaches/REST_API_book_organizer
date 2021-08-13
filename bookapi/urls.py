from django.urls import path
from . import views

urlpatterns = [
    path("create_user", views.create_user, name='create_user'),
    path("books", views.redirect_books, name='books'),
    path("book", views.redirect_book, name='book'),
    path("library", views.redirect_library, name='library')
]

# Possible routes: 
# ../admin/
# ../api-auth/login/
# ../api-auth/logout/
# ../bookapi/create_user/
# ../bookapi/book/
# ../bookapi/books/
# ../bookapi/library/