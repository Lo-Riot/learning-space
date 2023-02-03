from django.contrib.auth.views import LoginView
from django.urls import path
from . import views


urlpatterns = [
    path('', views.UserList.as_view(), name='users'),
    path('<int:pk>', views.UserDetail.as_view(), name='user'),
    path('login/', views.UserLogin.as_view(), name='login')
]
