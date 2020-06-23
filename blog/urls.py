from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('like', views.likes, name='like'),
    path('feed/', views.news_feed, name='news_feed'),
    path('user/<int:user_id>/', views.user_page, name='user page'),
]
