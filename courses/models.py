from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from account.models import User, Author


class Course(models.Model):
    name = models.CharField(max_length=50)
    author = models.ForeignKey(
        Author, related_name="courses", on_delete=models.CASCADE
    )
    description = models.CharField(max_length=250)
    rating = models.IntegerField(validators=[
        MinValueValidator(1), MaxValueValidator(10)
    ], default=0)
    image = models.ImageField(upload_to='uploads/')


class Enrollment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Lesson(models.Model):
    name = models.CharField(max_length=50)
    content = models.TextField()
    video = models.FileField(upload_to='uploads/', null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)


class Comment(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=500)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)


class Task(models.Model):
    name = models.CharField(max_length=50)
    content = models.TextField()
    solution_file = models.FileField(upload_to='uploads/')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
