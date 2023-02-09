from django.urls import path
from . import views


urlpatterns = [
    path(
        'courses/',
        views.CourseList.as_view(), name='courses'
    ),
    path(
        'courses/<int:course_pk>/',
        views.CourseDetail.as_view(), name='course'
    ),
    path(
        'courses/<int:course_pk>/lessons/',
        views.LessonList.as_view(), name='lessons'
    ),
    path(
        'courses/<int:course_pk>/lessons/<int:lesson_pk>/',
        views.LessonDetail.as_view(), name='lesson'
    ),
    path(
        'users/<int:pk>/enrollments/',
        views.EnrollmentList.as_view(), name='enrollments'
    ),
]
