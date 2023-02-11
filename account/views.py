from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status

from account.models import User, Author
from account.serializers import UserSerializer, AuthorSerializer


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.filter(author__isnull=True)
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.filter(author__isnull=True)
    serializer_class = UserSerializer


class AuthorList(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class AuthorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


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
