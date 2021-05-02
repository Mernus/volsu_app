from rest_framework import serializers

from main.models import Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = [
            "title", "back_color", "title_color"
        ]
