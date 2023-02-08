from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import generics, status, permissions
from courses.permissions import IsAuthorOrReadOnly

from courses.models import Course, Lesson
from courses.serializers import CourseSerializer, LessonSerializer


class CourseList(generics.ListCreateAPIView):
    """List all courses"""
    serializer_class = CourseSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnly
    ]
    queryset = Course.objects.all()

    def post(self, request):
        serializer = CourseSerializer(
            data=request.data, context={'user': request.user}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseDetail(APIView):
    """Create, get, update or delete a course"""
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnly
    ]
    parser_classes = [MultiPartParser]

    def get(self, request, course_pk):
        course = get_object_or_404(Course, pk=course_pk)
        serializer = CourseSerializer(course)
        return Response(serializer.data)

    def put(self, request, course_pk):
        course = get_object_or_404(Course, pk=course_pk)
        self.check_object_permissions(request, course)
        serializer = CourseSerializer(course, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, course_pk):
        course = get_object_or_404(Course, pk=course_pk)
        self.check_object_permissions(request, course)
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LessonList(generics.ListCreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnly
    ]

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
    lookup_url_kwarg = "lesson_pk"
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
