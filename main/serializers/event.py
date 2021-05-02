from rest_framework import serializers

from main.models import Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            "title", "author", "participants",
            "tags", "start_date", "end_date", "status"
        ]
