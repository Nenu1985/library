from django.shortcuts import render, HttpResponseRedirect, redirect
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from library.models import Book
from django.urls import reverse_lazy
from library.forms import BookCreateForm
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
# Create your views here.


class UserListView(FormView):
    # queryset = User.objects.filter(is_active=True)
    template_name = 'library/users_list.html'
    # context_object_name = 'users'
    form_class = UserCreationForm
    model = User
    success_url = reverse_lazy('library:users-list')

    def get_context_data(self, **kwargs):
        kwargs['users'] = User.objects.filter(is_active=True)
        return super(UserListView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=raw_password)
        login(self.request, user)
        # return redirect('home')
        super().form_valid(form)



class BookListView(ListView):
    queryset = Book.objects.all()
    template_name = 'library/book_list.html'
    context_object_name = 'books'


class BookDetailView(DetailView):
    model = Book


class BookCreateView(CreateView):
    model = Book
    template_name = 'library/create_book.html'
    # success_url = reverse_lazy('library:users-list')
    form_class = BookCreateForm

    def get_context_data(self, **kwargs):
        kwargs['books'] = Book.objects.order_by('created')
        return super(BookCreateView, self).get_context_data(**kwargs)

    @method_decorator(csrf_protect, login_required)
    def post(self, request, *args, **kwargs):

        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            new_item = form.save(commit=False)
            new_item.user = self.request.user
            new_item.save()
            return HttpResponseRedirect(reverse_lazy('library:books-list'))
        return super(BookCreateView, self).post(request, *args, **kwargs)


