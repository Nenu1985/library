from django import forms
from .models import Book
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.utils import timezone
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator


class UserCreateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')


class BookCreateForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('author', 'title',
                  'description', 'published_year',
                  'poster',)

    def clean(self):
        self.cleaned_data = super().clean()
        is_same_book_exists = Book.objects.filter(slug=slugify(self.cleaned_data['title']),
                                                  author=self.cleaned_data['author'],
                                                  published_year=self.cleaned_data['published_year'],
                                                  )
        if is_same_book_exists:
            raise forms.ValidationError('A book with the same parameters '
                                        'already exists in the database!')

    def save(self, force_insert=False,
             force_update=False,
             commit=True):
        book = super(BookCreateForm, self).save(commit=False)

        if commit:
            book.save()
        return book
