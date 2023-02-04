from django.urls import path
from . import views


urlpatterns = [
    path('courses/', views.CourseList.as_view(), name='courses'),
    path('courses/<int:pk>/', views.CourseDetail.as_view(), name='course'),
]
