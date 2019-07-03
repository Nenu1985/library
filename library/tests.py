from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from django.contrib.auth import authenticate
from library.models import Book
from django.urls import reverse
from django.utils import timezone
import pprint

# Create your tests here.
class LibTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_user_creation(self):
        url = reverse('library:users-list')
        data = {
            'username': 'u_john',
            'first_name': 'f_john',
            'last_name': 'l_john',
        }
        resp = self.client.post(url, data=data)

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(1, User.objects.count())
        self.assertEqual('u_john', User.objects.first().username)

    def test_book_creation_and_upload_file(self):

        john = User.objects.create_user(username='john_',
                                        first_name='fjohn',
                                        last_name='ljohn')

        self.assertEqual(1, User.objects.count())

        url = reverse('library:user-detail', kwargs={'username': john.username})

        with open('library/test_img.jpg', 'rb') as fp:
            data = {
                'author': 'John Smith',
                'title': 'Python for kids',
                'description': 'This book about python',
                'published_year': 2013,
                'poster': fp,
            }
            resp = self.client.post(url, data)

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(1, john.books.count())

        book = john.books.first()
        self.assertEqual('This book about python', book.description)

    def test_update_book(self):
        john = User.objects.create_user(username='john_',
                                        first_name='fjohn',
                                        last_name='ljohn')

        self.assertEqual(1, User.objects.count())

        url = reverse('library:user-detail', kwargs={'username': john.username})

        with open('library/test_img.jpg', 'rb') as fp:
            book = Book(
                author='John Smith',
                title='Python for kids',
                description='This book about python',
                published_year=2013,
                user=john,
            )
            book.poster.save('image_name', fp)
            book.save()
            john.books.add(book)

        self.assertEqual(1, john.books.count())
        self.assertEqual(book.slug, 'python-for-kids')
        book = john.books.first()

        # url = book.get_absolute_url()
        url = reverse('library:book-update', kwargs={
            'id': book.id,
            'slug': book.slug,
        })
        self.assertEqual(url, '/books/1/python-for-kids/')


         # Data to update book
        with open('library/test_img.jpg', 'rb') as file:
            new_data = {
                'user': john.id,
                'author': 'new author',
                'title': 'Python not for kids',
                'description': 'This book about python',
                'published_year': '2013',
                'poster': file,
                # 'slug': 'python-not-for-kids',
                # 'created': timezone.now(),
            }
            # POST: update book with new data
            resp = self.client.post(url, new_data)

        self.assertEqual(resp.status_code, 302)

        book.refresh_from_db()

        self.assertEqual(book.title, 'Python not for kids')
        self.assertEqual(book.slug, 'python-not-for-kids')
        self.assertEqual(book.author, 'new author')
