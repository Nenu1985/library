from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.views.generic import ListView, DetailView, FormView, View, UpdateView
from django.contrib.auth.models import User
from library.models import Book
from django.urls import reverse_lazy
from library.forms import BookCreateForm, UserCreateForm
from django.utils.text import slugify

# Create your views here.


class UsersView(FormView):
    template_name = 'library/users_list.html'
    form_class = UserCreateForm
    model = User
    success_url = reverse_lazy('library:users-list')

    def get_context_data(self, **kwargs):
        kwargs['users'] = User.objects.filter(is_active=True)
        return super(UsersView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


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
            if book:
                user.books.add(book)
        return HttpResponseRedirect(reverse_lazy('library:user-detail',
                                                 kwargs={'username': user.username}))


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
