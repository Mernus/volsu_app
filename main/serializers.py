from rest_framework import serializers

from .models import User, Tag, Event


# TODO переработать после обновы
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["name", "fullname", "timezone", "email", "level"]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["title", "back_color", "title_color"]


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ["title", "author", "participants", "tags", "start_date", "end_date", "status"]
