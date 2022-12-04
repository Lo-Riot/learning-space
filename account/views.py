from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import generics, status

from account.models import User
from account.serializers import UserSerializer


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
