from rest_framework import serializers
from courses.models import Course


class CourseSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=50)
    description = serializers.CharField(max_length=250)
    rating = serializers.IntegerField(read_only=True)
    image = serializers.ImageField(required=False)
    creator = serializers.ReadOnlyField(source='creator.user.username')

    def create(self, validated_data):
        return Course.objects.create(
            **validated_data, creator=self.context["user"].id
        )

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get(
            'description', instance.description
        )
        instance.save()
        return instance
