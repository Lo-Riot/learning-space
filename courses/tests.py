from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from account.models import User, Author
from courses.models import Course
from courses.serializers import CourseSerializer


class CourseCreateTestCase(APITestCase):
    def setUp(self):
        user_data = {'username': "TestUser", 'password': "test"}
        user = User.objects.create_user(**user_data)
        author = Author.objects.create(user=user)

        self.user_cookies = self.client.post(
            reverse('login'), data=user_data
        ).cookies
        self.course_data = {
            'name': "TestCourse",
            'description': "Course description",
            'author': author.pk
        }

    def test_course_create_without_image(self):
        response = self.client.post(
            reverse('courses'),
            data=self.course_data,
            cookies=self.user_cookies
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class CourseTestCase(APITestCase):
    def setUp(self):
        user_data = {'username': "TestUser", 'password': "test"}
        user = User.objects.create_user(**user_data)
        author = Author.objects.create(user=user)

        self.user_cookies = self.client.post(
            reverse('login'), data=user_data
        ).cookies
        self.course_data = {
            'name': "TestCourse",
            'description': "Course description",
            'author': author
        }
        self.course = Course.objects.create(**self.course_data)
        self.serializer = CourseSerializer(self.course)

    def test_course_list(self):
        response = self.client.get(reverse('courses'))
        self.assertEqual(response.data, [self.serializer.data])

    def test_course_detail(self):
        response = self.client.get(reverse('course', args=[self.course.pk]))
        self.assertEqual(response.data, self.serializer.data)

    def test_course_update(self):
        updated_course_data = {
            'name': "TestCourse",
            'description': "Description is updated",
        }

        self.assertNotEqual(
            self.course.description,
            updated_course_data['description']
        )
        self.course.description = updated_course_data['description']

        response = self.client.put(
            reverse('course', args=[self.course.pk]),
            data=updated_course_data,
            cookies=self.user_cookies
        )
        self.assertEqual(response.data, self.serializer.data)
