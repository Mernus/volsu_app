from rest_framework import serializers

from main.models import EVENT_STATUSES, Event
from main.serializers.mixins import DateTimeFieldWihTZ


class EventSerializer(serializers.ModelSerializer):
    status_name = serializers.ChoiceField(source='get_status_display', choices=EVENT_STATUSES)
    author_name = serializers.StringRelatedField(source='author.get_short_name', read_only=True)
    author_image = serializers.ImageField(source='author.profile_img', read_only=True)
    author_org = serializers.StringRelatedField(source='author.organization', read_only=True)
    start_date_aware = DateTimeFieldWihTZ(source='start_date', read_only=True)
    end_date_aware = DateTimeFieldWihTZ(source='end_date', read_only=True)
    all_tags = serializers.ListField(source='get_all_tags_html', read_only=True)
    first_image = serializers.CharField(source='get_first_image_url', read_only=True)
    files = serializers.ListField(source='get_files_url', read_only=True)

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
            "status_name", "eventfile_set", "author_image",
            "author_org", "all_tags", "first_image", "files"
        ]

        read_only_fields = [
            "start_date_aware", "end_date_aware", "author_image",
            "slug", "author_org", "author_name", "all_tags",
            "first_image", "files"
        ]


class ListEventSerializer(serializers.ModelSerializer):
    status_name = serializers.ChoiceField(source='get_status_display', choices=EVENT_STATUSES)
    author_fullname = serializers.StringRelatedField(source='author', read_only=True)
    author_image = serializers.ImageField(source='author.profile_img', read_only=True)
    first_image = serializers.CharField(source='get_first_image_url', read_only=True)
    participants_number = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            "title", "description", "get_popular_tags_html",
            "start_date", "end_date", "slug", "participants_number",
            "eventfile_set", "status_name", "author_image",
            "first_participants", "author_fullname", "first_image"
        ]

        read_only_fields = ["first_image", "participants_number"]

    # TODO docs
    def get_participants_number(self, obj) -> int:
        return obj.participants.all().count()
