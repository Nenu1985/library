from django.urls import path
from library import views

app_name = 'libproj'

urlpatterns = [
    path("", views.UserListView.as_view(), name='users-list'),


]

