from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('books/', views.book_list, name='book_list'),
    path('books/category/<uslug:slug>/', views.book_category_detail, name='book_category_detail'),
    path('books/<uslug:slug>/', views.book_detail, name='book_detail'),
    path('movies/', views.movie_list, name='movie_list'),
    path('movies/category/<uslug:slug>/', views.movie_category_detail, name='movie_category_detail'),
    path('movies/<uslug:slug>/', views.movie_detail, name='movie_detail'),
]

