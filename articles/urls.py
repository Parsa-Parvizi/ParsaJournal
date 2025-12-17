from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    path('', views.article_list, name='article_list'),
    path('article/<uslug:slug>/', views.article_detail, name='article_detail'),
    path('category/<uslug:slug>/', views.category_detail, name='category_detail'),
    path('tag/<uslug:slug>/', views.tag_detail, name='tag_detail'),
    path('author/<uslug:slug>/', views.author_detail, name='author_detail'),
]

