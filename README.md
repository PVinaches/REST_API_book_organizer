## Book organizer REST API project:

<div style="text-align: justify">
    This REST API application is a collaborative book organizer, using python Django framework, Django REST framework and PostgreSQL database. The users will add individual books to create a shared library and, then, archive them in their library database.
</div>

#### Requirements
[Python 3 (Anaconda for linux v.2.0.4)](https://anaconda.cloud/installers) 
[Django v.3.2.5](https://www.djangoproject.com/download/)
[Django Rest Framework v.3.12.4](https://www.django-rest-framework.org/#installation)
[PostgreSQL v.12.7](https://www.postgresql.org/download/linux/ubuntu/)
[Psycopg2 v.2.9.1](https://pypi.org/project/psycopg2/)

#### Usage

Once installed the requirements, execute the following:
- python manage.py makemigrations bookapi
- python manage.py migrate
- python manage.py runserver

##### Files description

- models.py and admin.py

<div style="text-align: justify">
    It contains four models, all registered into admin.py. The User standard model is for recording the users. The Book model includes the different book data (title, author). The BookCreator model is a table that relates the user from the User model that added the book into the Book model. Finally, the Library model registers the books from the Book model into a personal database.
    <br></br>
</div>

- serializers.py

<div style="text-align: justify">
    The three custom models (Book, BookCreator and Library) have their own custom serializers described in this file.
    <br></br>
</div>

- permission.py

<div style="text-align: justify">
    The IsOwner function is defined to control the permission of to modify/delete the books added to the Book model.
    <br></br>
</div>

- test_models.py

<div style="text-align: justify">
    The four models are tested according to the instructions described in this file. Each test has a setup entering new data into the model and, following, the test getting the information.
    <br></br>
</div>

- test_views.py

<div style="text-align: justify">
    The views are tested according to the instructions described in this file. Each test has a setup entering new data into the different models (for methods get, put and delete) and the expected answer. The test calls the different views and compares the expected answer with the one provided by the view. When authentication is needed, .force_login() is used.
    <br></br>
</div>

- views.py

<div style="text-align: justify">
    The first view (create_user) allows the user to create an account. It is the only view that allows any request.
    <br></br>
</div>

<div style="text-align: justify">
    The second view (redirect_books) calls the function get_all_books or add_book depending on the request method. The first function returns all the books from the Book model. The second function allows adding a new book into the Book model, also creating a register into the BookCreator model.
    <br></br>
</div>

<div style="text-align: justify">
    The third view (redirect_book) checks the IsOwner permission, and if allowed, it calls the function get_book, update_book or delete_book, depending on the request method. The first function returns the complete information of just one book, the second allows modifying it, and the third deletes it.
    <br></br>
</div>

<div style="text-align: justify">
    Finally, the fourth view (redirect_library) calls the function get_all_books_library, add_book_library or delete_book_library depending on the request method. The first function returns the complete information of the user's library, the second, allows adding a new entry, and the third, deletes it.
    <br></br>
</div>