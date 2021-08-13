from .models import BookCreator

def IsOwner(request):
    book_added = request.data.get('title')
    book_creator = BookCreator.objects.filter(book_added=book_added, poster=request.user.username)
    return (True if book_creator else False)