from django.contrib import admin
from library.models import Book


# Register your models here.
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['author', 'title', 'slug',
                    'description',
                    'poster', 'user']
    list_filter = ['created']