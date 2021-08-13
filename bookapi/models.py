from django.db import models
from django.contrib.auth.models import AbstractUser

# User model for authentication
class User(AbstractUser):
    pass

# Books model for repository
class Book(models.Model):
    title = models.TextField(max_length=500)
    author = models.CharField(max_length=255)
    year = models.IntegerField()
    language = models.CharField(max_length=255)
    editorial = models.TextField(max_length=500)
    ISBN = models.CharField(max_length=30)

    def __repr__(self):
        return f"{self.title}, {self.author}, {self.year}, {self.language}, {self.editorial}, {self.ISBN}"

# Book creator identifier
class BookCreator(models.Model):
    poster = models.CharField(max_length=255)
    book_added = models.CharField(max_length=500)

    def __repr__(self):
        return self.book_added + ' was added by ' + self.poster

# Personal repository
class Library(models.Model):
    user_name = models.CharField(max_length=255)
    title_book = models.CharField(max_length=500)

    def __repr__(self):
        return self.title_book + ' was added to the library.'