from rest_framework import serializers

from main.models import EVENT_STATUSES, Event
from main.serializers.mixins import DateTimeFieldWihTZ


class EventSerializer(serializers.ModelSerializer):
    status_name = serializers.ChoiceField(source='get_status_display', choices=EVENT_STATUSES)
    author_name = serializers.StringRelatedField(source='author.get_short_name', read_only=True)
    author_image = serializers.URLField(source='author.profile_img', read_only=True)
    author_org = serializers.StringRelatedField(source='author.organization', read_only=True)
    start_date_aware = DateTimeFieldWihTZ(source='start_date', read_only=True)
    end_date_aware = DateTimeFieldWihTZ(source='end_date', read_only=True)
    all_tags = serializers.ListField(source='get_all_tags_html', read_only=True)

    def __init__(self, *args, **kwargs):
        self.request = kwargs['context'].pop('request')
        super(EventSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = Event
        lookup_field = 'slug'
        fields = [
            "title", "description", "location", "tags",
            "website", "get_tags_html", "author_name", "slug",
            "participants", "start_date_aware", "end_date_aware",
            "status_name", "event_files", "author_image",
            "author_org", "all_tags"
        ]

        read_only_fields = [
            "start_date_aware", "end_date_aware", "author_image",
            "slug", "author_org", "author_name", "all_tags"
        ]


class ListEventSerializer(serializers.ModelSerializer):
    status_name = serializers.ChoiceField(source='get_status_display', choices=EVENT_STATUSES)
    author_fullname = serializers.StringRelatedField(source='author', read_only=True)
    author_image = serializers.URLField(source='author.profile_img', read_only=True)

    class Meta:
        model = Event
        fields = [
            "title", "description", "get_popular_tags_html",
            "start_date", "end_date", "slug",
            "event_files", "status_name", "author_image",
            "first_participants", "author_fullname"
        ]