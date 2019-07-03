from django.urls import path
from library import views

app_name = 'library'

urlpatterns = [
    path('', views.UserListView.as_view(), name='users-list'),
    path('books/', views.BookCreateView.as_view(), name='books-list'),
    path('books/<int:id>/<slug:slug>/', views.BookDetailView.as_view(), name='book-detail'),
path('user/',)

]

