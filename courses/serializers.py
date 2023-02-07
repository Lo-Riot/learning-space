from rest_framework import serializers
from courses.models import Course, Lesson
from account.models import Author


class CourseSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=50)
    description = serializers.CharField(max_length=250)
    rating = serializers.IntegerField(read_only=True)
    image = serializers.ImageField(required=False)
    author = serializers.PrimaryKeyRelatedField(
        source='author.pk', read_only=True
    )

    def create(self, validated_data):
        return Course.objects.create(
            **validated_data,
            author=Author.objects.get(user_id=self.context["user"].id)
        )

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get(
            'description', instance.description
        )
        instance.save()
        return instance


class LessonSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=50)
    content = serializers.CharField()
    course = serializers.PrimaryKeyRelatedField(
        source='course.pk', read_only=True
    )

    def create(self, validated_data):
        return Lesson.objects.create(
            **validated_data,
            course=Course.objects.get(pk=self.context["course_pk"])
        )

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.content = validated_data.get('content', instance.content)
        instance.save()
        return instance
