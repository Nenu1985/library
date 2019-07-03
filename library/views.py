from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User
from library.models import Book
# Create your views here.


class UserListView(ListView):
    queryset = User.objects.filter(is_active=True)
    template_name = 'library/users_list.html'
    context_object_name = 'users'


class BookListView(ListView):
    queryset = Book.objects.all()
    template_name = 'library/book_list.html'
    context_object_name = 'books'


class BookDetailView(DetailView):
    model = Book