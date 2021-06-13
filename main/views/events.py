from django.db.models import Q
from rest_framework import mixins
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.viewsets import GenericViewSet

from main.models import Event, Tag, USER_LEVELS
from main.pagination import BasePagination
from main.serializers import EventSerializer, ListEventSerializer
from main.utils import render_tags


class EventsPagination(BasePagination):
    page_size = 6


class EventListViewSet(mixins.ListModelMixin, GenericViewSet):
    pagination_class = EventsPagination
    renderer_classes = [TemplateHTMLRenderer, ]
    serializer_class = ListEventSerializer
    permission_classes = []

    # TODO Move to base class
    def get_queryset(self):
        current_user = self.request.user
        if current_user.is_authenticated:
            if current_user.level in [USER_LEVELS.MODERATOR, USER_LEVELS.ADMIN]:
                return Event.objects.all()
            return Event.objects.filter(Q(author__isnull=False), Q(author=current_user) | Q(status__in=[1, 2, 3]))

        return Event.public_objects.all()

    def list(self, request, *args, **kwargs):
        response = super(EventListViewSet, self).list(request, *args, **kwargs)
        response.template_name = 'event/events_list.html'

        queryset = self.filter_queryset(self.get_queryset())
        response.data['all'] = queryset.count()

        return response


event_list = EventListViewSet.as_view({'get': 'list'})


class EventDetailViewSet(mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         GenericViewSet):
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    serializer_class = EventSerializer
    permission_classes = []
    lookup_field = 'slug'

    # TODO Move to base class
    def get_queryset(self):
        current_user = self.request.user
        if current_user.is_authenticated:
            if current_user.level in [USER_LEVELS.MODERATOR, USER_LEVELS.ADMIN]:
                return Event.objects.all()
            return Event.objects.filter(Q(author__isnull=False), Q(author=current_user) | Q(status__in=[1, 2, 3]))

        return Event.public_objects.all()

    def retrieve(self, request, *args, **kwargs):
        response = super(EventDetailViewSet, self).retrieve(request, *args, **kwargs)
        response.template_name = 'event/event_detail.html'

        event_tags = Event.objects.get(title=response.data['title']).tags.values_list('title', flat=True)
        sorted_tags = sorted(Tag.objects.exclude(title__in=event_tags).all(),
                             key=lambda some_tag: some_tag.events_num, reverse=True)
        response.data['all_tags'] = render_tags(sorted_tags)

        return response


event_detail = EventDetailViewSet.as_view({
    'get': 'retrieve',
    'patch': 'partial_update'
})
