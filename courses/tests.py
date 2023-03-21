from io import BytesIO
from PIL import Image
import os

from django.conf import settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from account.models import User, Author
from courses.models import Course, Lesson
from courses.serializers import (
    CourseSerializer, EnrollmentSerializer, LessonSerializer
)


def generate_image(filename: str, size: tuple = (1, 1)) -> BytesIO:
    file_obj = BytesIO()
    image = Image.new("RGBA", size, (0, 0, 0))
    image.save(file_obj, "png")
    file_obj.name = filename
    file_obj.seek(0)
    return file_obj


def remove_image(uploaded_image_filename: str) -> None:
    uploaded_image_path = settings.MEDIA_ROOT / uploaded_image_filename
    if os.path.isfile(uploaded_image_path):
        os.remove(uploaded_image_path)


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
        super().setUp()
        self.course_data = {
            'name': "TestCourse",
            'description': "Course description",
            'image': generate_image("test.png"),
        }
        self.uploaded_image_filename = ''

    def tearDown(self):
        super().tearDown()
        # TODO: Remove this method, use 'remove_image' function
        # inside the 'test_course_create'
        remove_image(self.uploaded_image_filename)

    def test_course_create(self):
        self.client.force_login(self.author.user)

        response = self.client.post(
            reverse('courses'),
            data=self.course_data,
        )
        self.uploaded_image_filename = response.data["image"]
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["author"], self.author.pk)

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

        response = self.client.get(
            reverse('courses'),
            data={'author': self.author.user.username}
        )
        self.assertEqual(response.data, [self.serializer.data])

    def test_course_list_order(self):
        courses = Course.objects.bulk_create([
            Course(
                name="TestCourse2",
                description="Course description 2",
                author=self.author
            ),
            Course(
                name="TestCourse3",
                description="Course description 3",
                author=self.author
            ),
        ])
        self.serializer = CourseSerializer(courses, many=True)

        response = self.client.get(
            reverse('courses'),
            data={'order': "-id"}
        )
        self.assertEqual(response.data[0], self.serializer.data[-1])

    def test_course_list_by_name(self):
        response = self.client.get(  # Filter courses by name "Test"
            reverse('courses'),
            data={'name': self.course.name[:4]}
        )
        self.assertEqual(response.data, [self.serializer.data])

    def test_course_detail(self):
        response = self.client.get(reverse('course', args=[self.course.pk]))
        self.assertEqual(response.data, self.serializer.data)

    def test_course_update(self):
        response = self.client.put(
            reverse('course', args=[self.course.pk]),
            data={
                'name': "TestCourse",
                'description': "Description is updated",
            }
        )
        self.assertNotEqual(
            response.data["description"], self.serializer.data["description"]
        )

    def test_course_partial_update(self):
        response = self.client.patch(
            reverse('course', args=[self.course.pk]),
            data={'rating': 7}
        )
        self.assertNotEqual(
            response.data["rating"], self.serializer.data["rating"]
        )

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

    def test_lesson_delete(self):
        response = self.client.delete(reverse(
            'lesson', args=[self.course.pk, self.lesson.pk]
        ))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class EnrollmentCreateTestCase(APITestCase):
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
        cls.unauth_user = User.objects.create_user(
            username="TestUnauthUser",
            password="test"
        )

    def setUp(self):
        self.client.force_login(self.unauth_user)

    def test_enroll(self):
        response = self.client.post(
            reverse('enrollments', args=[self.unauth_user.pk]),
            data={'course': self.course.pk}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class EnrollmentTestCase(APITestCase):
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
        cls.unauth_user = User.objects.create_user(
            username="TestUnauthUser",
            password="test"
        )
        cls.enrollment = cls.unauth_user.enrollment_set.create(
            course=cls.course
        )

    def setUp(self):
        self.client.force_login(self.author.user)
        self.serializer = EnrollmentSerializer(self.enrollment)

    def test_enrollment_list(self):
        response = self.client.get(reverse(
            'enrollments', args=[self.unauth_user.pk]
        ))
        self.assertEqual(response.data, [self.serializer.data])
