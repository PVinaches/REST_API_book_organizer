from rest_framework import serializers
from .models import Book, BookCreator, Library

# Serializer for book model
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('title', 'author', 'year', 'language', 'editorial', 'ISBN')

# Serializer for book creator model
class BookCreatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookCreator
        fields = ('poster', 'book_added')

# Serializer for library model
class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Library
        fields = ('user_name', 'title_book')