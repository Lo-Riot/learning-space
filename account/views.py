from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status

from account.models import User
from account.serializers import UserSerializer


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserLogin(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if request.user.is_authenticated:
            return Response(status=status.HTTP_200_OK)
        elif serializer.is_valid():
            user = authenticate(request, **serializer.validated_data)
            if user is not None:
                login(request, user)
                return Response(status=status.HTTP_200_OK)

        return Response(
            data=serializer.errors, status=status.HTTP_401_UNAUTHORIZED
        )
