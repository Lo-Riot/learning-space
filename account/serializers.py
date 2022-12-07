from rest_framework import serializers
from .models import User, Creator


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(source='user.id', read_only=True)
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    courses = serializers.PrimaryKeyRelatedField(many=True, read_only=True)


class CreatorSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='user.id', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    courses = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Creator
        fields = ['id', 'username', 'courses']
