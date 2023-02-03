from django.contrib.auth.views import LoginView
from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.UserLogin.as_view(), name='login'),
    path('users/', views.UserList.as_view(), name='users'),
    path('users/<int:pk>/', views.UserDetail.as_view(), name='user'),

    path('authors/', views.AuthorList.as_view(), name='authors'),
    path('authors/<int:pk>/', views.AuthorDetail.as_view(), name='author'),
]
