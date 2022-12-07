from django.contrib.auth.views import LoginView
from django.urls import path
from . import views


urlpatterns = [
    path('', views.UserList.as_view()),
    path('<int:pk>', views.UserDetail.as_view()),
    path('login/', views.UserLogin.as_view())
]
