from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from courses.permissions import IsCreatorOrReadOnly

from courses.models import Course
from courses.serializers import CourseSerializer


class CourseList(APIView):
    """List all courses"""
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsCreatorOrReadOnly
    ]

    def get(self, request):
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

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
        IsCreatorOrReadOnly
    ]

    def get(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        serializer = CourseSerializer(course)
        return Response(serializer.data)

    def put(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        self.check_object_permissions(request, course)
        serializer = CourseSerializer(course, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        course = get_object_or_404(Course, pk)
        self.check_object_permissions(request, course)
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
