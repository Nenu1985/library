from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User
# Create your views here.


class UserListView(ListView):
    queryset = User.objects.filter(is_active=True)
    template_name = 'library/users_list.html'
    context_object_name = 'users'