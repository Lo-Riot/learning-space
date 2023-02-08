from django.urls import reverse
from django.conf import settings
from rest_framework import status
from rest_framework.test import APITestCase

from account.models import User, Author
from courses.models import Course, Lesson
from courses.serializers import CourseSerializer, LessonSerializer


class CourseCreateTestCase(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        user = User.objects.create_user(
            username="TestUser",
            password="test"
        )
        cls.author = Author.objects.create(user=user)
        cls.unauth_user = User.objects.create_user(
            username="TestUnauthUser",
            password="test"
        )

    def setUp(self):
        self.course_data = {
            'name': "TestCourse",
            'description': "Course description",
        }

    def test_course_create_without_image(self):
        self.client.force_login(self.author.user)

        response = self.client.post(
            reverse('courses'),
            data=self.course_data,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['author'], self.author.pk)

    def test_course_create_with_image(self):
        self.client.force_login(self.author.user)

        with open(settings.MEDIA_ROOT / "uploads/test.jpg", 'rb') as image:
            updated_course_data = {'image': image}
            updated_course_data.update(self.course_data)

            response = self.client.post(
                reverse('courses'),
                data=updated_course_data,
            )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['author'], self.author.pk)

    def test_course_create_unauth(self):
        self.client.force_login(self.unauth_user)

        response = self.client.post(
            reverse('courses'),
            data=self.course_data,
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class CourseTestCase(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        user = User.objects.create_user(
            username="TestUser",
            password="test"
        )
        cls.author = Author.objects.create(user=user)
        cls.course = Course.objects.create(
            name="TestCourse",
            description="Course description",
            author=cls.author,
        )

    def setUp(self):
        self.client.force_login(self.author.user)
        self.serializer = CourseSerializer(self.course)

    def test_course_list(self):
        response = self.client.get(reverse('courses'))
        self.assertEqual(response.data, [self.serializer.data])

    def test_course_detail(self):
        response = self.client.get(reverse('course', args=[self.course.pk]))
        self.assertEqual(response.data, self.serializer.data)

    def test_course_update(self):
        self.course.description = "Description is updated"

        response = self.client.put(
            reverse('course', args=[self.course.pk]),
            data={'name': "TestCourse", 'description': self.course.description}
        )
        self.assertEqual(response.data, self.serializer.data)

    def test_course_delete(self):
        response = self.client.delete(reverse('course', args=[self.course.pk]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class LessonCreateTestCase(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        user = User.objects.create_user(
            username="TestUser",
            password="test"
        )
        cls.author = Author.objects.create(user=user)
        cls.course = Course.objects.create(
            name="TestCourse",
            description="Course description",
            author=cls.author,
        )
        cls.lesson_data = {
            'name': "TestLesson",
            'content': "Lesson content",
        }

    def setUp(self):
        self.client.force_login(self.author.user)

    def test_lesson_create(self):
        response = self.client.post(
            reverse('lessons', args=[self.course.pk]),
            data=self.lesson_data,
        )
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED, msg=response.data
        )


class LessonTestCase(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        user = User.objects.create_user(
            username="TestUser",
            password="test"
        )
        cls.author = Author.objects.create(user=user)
        cls.course = Course.objects.create(
            name="TestCourse",
            description="Course description",
            author=cls.author,
        )
        cls.lesson = Lesson.objects.create(
            name="TestLesson",
            content="Lesson content",
            course=cls.course,
        )

    def setUp(self):
        self.client.force_login(self.author.user)
        self.serializer = LessonSerializer(self.lesson)

    def test_lesson_list(self):
        response = self.client.get(reverse('lessons', args=[self.course.pk]))
        self.assertEqual(response.data, [self.serializer.data])

    def test_lesson_detail(self):
        response = self.client.get(reverse(
            'lesson', args=[self.course.pk, self.lesson.pk]
        ))
        self.assertEqual(response.data, self.serializer.data)

    def test_lesson_update(self):
        self.lesson.content = "Updated lesson content"

        response = self.client.put(
            reverse('lesson', args=[self.course.pk, self.lesson.pk]),
            data={'name': "TestLesson", 'content': self.lesson.content},
        )
        self.assertEqual(response.data, self.serializer.data)

    def test_course_delete(self):
        response = self.client.delete(reverse(
            'lesson', args=[self.course.pk, self.lesson.pk]
        ))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
