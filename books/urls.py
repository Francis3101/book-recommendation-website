from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('book/<str:book_id>/', views.book_detail, name='book_detail'),
    path('search/', views.search_books, name='search_books'),
]