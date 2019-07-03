from django.shortcuts import render, HttpResponseRedirect, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, FormView, View, UpdateView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from library.models import Book
from django.urls import reverse_lazy
from library.forms import BookCreateForm, UserCreateForm
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.utils.text import slugify


# Create your views here.


class UsersView(FormView):
    # queryset = User.objects.filter(is_active=True)
    template_name = 'library/users_list.html'
    # context_object_name = 'users'
    form_class = UserCreateForm
    model = User
    success_url = reverse_lazy('library:users-list')

    def get_context_data(self, **kwargs):
        kwargs['users'] = User.objects.filter(is_active=True)
        return super(UsersView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        # username = form.cleaned_data.get('username')
        # first_name = form.cleaned_data.get('first_name')
        # last_name = form.cleaned_data.get('last_name')
        #
        # user = authenticate(username=username,
        #                     first_name=first_name,
        #                     last_name=last_name,)
        form.save()
        return super().form_valid(form)
        # login(self.request, user)
        # return redirect('home')


class UserDetailView(View):
    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        book_creation_form = BookCreateForm()
        return render(request, 'library/user_detail.html',
                      {'user': user,
                       'form': book_creation_form, })

    def post(self, request, username):
        form = BookCreateForm(request.POST, request.FILES)
        user = User.objects.get(username=username)
        form.instance.user = user
        if form.is_valid():
            book = form.save()
            user.books.add(book)

        return render(request, 'library/user_detail.html',
                      {'user': user,
                       'form': form, })


class BookListView(ListView):
    queryset = Book.objects.all()
    template_name = 'library/book_list.html'
    context_object_name = 'books'


class BookDetailView(DetailView):
    model = Book


class BookUpdateView(UpdateView):
    model = Book
    template_name = 'library/book_detail.html'
    fields = '__all__'
    context_object_name = 'book'
    success_url = reverse_lazy('library:users-list')

    def form_valid(self, form):
        form.slug = slugify(form.cleaned_data.get('title'))
        form.save()
        return super().form_valid(form)
    # success_url = reverse_lazy('library:users-list')
    # form_class = BookCreateForm
    #
    # def get_context_data(self, **kwargs):
    #     kwargs['books'] = Book.objects.order_by('created')
    #     return super(BookUpdateView, self).get_context_data(**kwargs)
    #
    # @method_decorator(csrf_protect, login_required)
    # def post(self, request, *args, **kwargs):
    #
    #     form = self.form_class(request.POST, request.FILES)
    #     if form.is_valid():
    #         new_item = form.save(commit=False)
    #         new_item.user = self.request.user
    #         new_item.save()
    #         return HttpResponseRedirect(reverse_lazy('library:books-list'))
    #     return super(BookUpdateView, self).post(request, *args, **kwargs)
    #
    #
