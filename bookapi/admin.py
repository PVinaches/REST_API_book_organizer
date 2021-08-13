from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Library, User, Book, BookCreator

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Book)
admin.site.register(BookCreator)
admin.site.register(Library)
