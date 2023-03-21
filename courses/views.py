from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import generics, status, permissions
from courses.permissions import IsAuthorOrReadOnly

from courses.models import Course, Enrollment, Lesson
from courses.serializers import (
    CourseSerializer, EnrollmentSerializer, LessonSerializer
)


class CourseList(generics.ListCreateAPIView):
    serializer_class = CourseSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnly
    ]
    parser_classes = [MultiPartParser]

    def get_queryset(self):
        name = self.request.query_params.get('name')
        author = self.request.query_params.get('author')
        order = self.request.query_params.get('order', "rating")
        queryset = Course.objects.all().order_by(order)
        # TODO: order by date

        if name is not None:
            queryset = queryset.filter(
                name__icontains=name
            )
        if author is not None:
            queryset = queryset.filter(
                author__user__username=author
            )
        return queryset

    def create(self, request):
        serializer = self.get_serializer(
            data=request.data, context={'user': request.user}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseDetail(generics.RetrieveUpdateDestroyAPIView):
    lookup_url_kwarg = "course_pk"
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnly
    ]

    def perform_update(self, serializer):
        serializer.save(partial=True)


class LessonList(generics.ListCreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnly
    ]
    parser_classes = [MultiPartParser]

    def get_queryset(self):
        return Lesson.objects.filter(course=self.kwargs["course_pk"])

    def post(self, request, course_pk):
        serializer = self.serializer_class(
            data=request.data, context={'course_pk': course_pk}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LessonDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LessonSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnly
    ]

    def get_queryset(self):
        return Lesson.objects.filter(course=self.kwargs["course_pk"])

    def get_object(self):
        obj = get_object_or_404(
            self.get_queryset(), pk=self.kwargs["lesson_pk"]
        )
        self.check_object_permissions(self.request, obj.course)
        return obj


class EnrollmentList(generics.ListCreateAPIView):
    serializer_class = EnrollmentSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
    ]

    def get_queryset(self):
        return Enrollment.objects.filter(user__id=self.kwargs["pk"])

    def post(self, request, pk):
        serializer = self.serializer_class(
            data=request.data, context={'user_pk': pk}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
