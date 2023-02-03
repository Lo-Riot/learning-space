from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from account.models import User
from account.serializers import UserSerializer


class UserTestCase(APITestCase):
    def setUp(self):
        self.user_data = {'username': "TestUser", 'password': "test"}

    def test_user_create(self):
        response = self.client.post(reverse('users'), data=self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_list(self):
        user = User.objects.create(**self.user_data)
        serializer = UserSerializer(user)
        response = self.client.get(reverse('users'))

        self.assertEqual(response.data, [serializer.data])

    def test_user_detail(self):
        user = User.objects.create(**self.user_data)
        serializer = UserSerializer(user)
        response = self.client.get(reverse('user', args=[user.pk]))

        self.assertEqual(response.data, serializer.data)

    def test_user_login(self):
        User.objects.create_user(**self.user_data)
        response = self.client.post(reverse('login'), data=self.user_data)

        self.assertEqual(
            response.status_code, status.HTTP_200_OK, msg=response.data
        )
