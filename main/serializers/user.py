from rest_framework import serializers

from main.models import User


# TODO менять поля, если это не текущий пользователь
class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username", "fullname",
            "organization", "timezone",
            "email", "level", "added",
            "updated"
        ]
        read_only_fields = [
            "level", "added", "updated"
        ]
        extra_kwargs = {'password': {'write_only': True}}


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "fullname",
            "organization",
            "level",
        ]
