from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth.models import User


# Create your models here.
class Book(models.Model):

    user = models.ForeignKey(User,
                             related_name='books',
                             on_delete=models.CASCADE)
    author = models.CharField(max_length=30)
    title = models.CharField(max_length=50)
    poster = models.ImageField(upload_to='books/%Y/%m/%d/')
    slug = models.SlugField(max_length=60, blank=True)
    description = models.TextField(blank=True)
    created = models.DateField(auto_now_add=True, db_index=True)

    def __str__(self):
        return str(self.title)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)  # slug generation for title
        super(Book, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('library:book-detail', args=[self.id])
