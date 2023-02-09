from rest_framework import serializers
from .models import User, Author


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    enrollments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        # TODO: The user should receive an e-mail to confirm password reset
        instance.password = validated_data.get('password', instance.password)


class AuthorSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(source='user.username')
    password = serializers.CharField(source='user.password', write_only=True)
    courses = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data["user"])
        return Author.objects.create(user=user)

    def update(self, instance, validated_data):
        # TODO: The author should receive an e-mail to confirm password reset
        instance.user.password = validated_data.get(
            'password', instance.user.password
        )
