from rest_framework import serializers
from .models import User, Author


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(source='user.id', read_only=True)
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    courses = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    def create(self, validated_data):
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # TODO: The user should receive an e-mail to confirm password reset
        instance.password = validated_data.get('password', instance.password)


class AuthorSerializer(serializers.Serializer):
    id = serializers.IntegerField(source='user.id', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    password = serializers.CharField(write_only=True)
    courses = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    def create(self, validated_data):
        return Author.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # TODO: The author should receive an e-mail to confirm password reset
        instance.password = validated_data.get('password', instance.password)
