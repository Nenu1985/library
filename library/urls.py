from django.urls import path
from library import views

app_name = 'library'

urlpatterns = [
    path('', views.UsersView.as_view(), name='users-list'),
    # path('books/', views.BookUpdateView.as_view(), name='book-update'),
    path('books/<int:id>/<slug:slug>/', views.BookUpdateView.as_view(), name='book-update'),
    path('user/<username>/', views.UserDetailView.as_view(), name='user-detail'),

]
