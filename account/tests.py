from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from account.models import User, Author
from account.serializers import UserSerializer, AuthorSerializer


class UserCreateTestCase(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_data = {'username': "TestUser", 'password': "test"}

    def test_user_create(self):
        response = self.client.post(reverse('users'), data=self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class UserTestCase(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_data = {'username': "TestUser", 'password': "test"}
        cls.user = User.objects.create_user(**cls.user_data)

    def setUp(self):
        self.serializer = UserSerializer(self.user)

    def test_user_list(self):
        response = self.client.get(reverse('users'))
        user = User.objects.get(pk=response.data[0]['id'])

        self.assertEqual(response.data, [self.serializer.data])
        self.assertFalse(hasattr(user, "author"))

    def test_user_detail(self):
        response = self.client.get(reverse('user', args=[self.user.pk]))
        user = User.objects.get(pk=response.data['id'])

        self.assertEqual(response.data, self.serializer.data)
        self.assertFalse(hasattr(user, "author"))

    def test_user_login(self):
        response = self.client.post(reverse('login'), data=self.user_data)
        self.assertEqual(
            response.status_code, status.HTTP_200_OK, msg=response.data
        )


class AuthorCreateTestCase(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_data = {'username': "TestUser", 'password': "test"}

    def test_author_create(self):
        response = self.client.post(reverse('authors'), data=self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class AuthorTestCase(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        user = User.objects.create_user(
            username="TestUser",
            password="test"
        )
        cls.author = Author.objects.create(user=user)

    def setUp(self):
        self.serializer = AuthorSerializer(self.author)

    def test_author_list(self):
        response = self.client.get(reverse('authors'))
        self.assertEqual(response.data, [self.serializer.data])

    def test_author_detail(self):
        response = self.client.get(reverse('author', args=[self.author.pk]))
        self.assertEqual(response.data, self.serializer.data)
