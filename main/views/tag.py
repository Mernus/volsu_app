from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.viewsets import GenericViewSet

from main.models import Tag
from main.pagination import BasePagination
from main.serializers import TagSerializer


class TagPagination(BasePagination):
    page_size = 8


class TagListViewSet(mixins.ListModelMixin, GenericViewSet):
    pagination_class = TagPagination
    renderer_classes = [TemplateHTMLRenderer, ]
    serializer_class = TagSerializer
    permission_classes = []
    queryset = Tag.objects.all()

    def list(self, request, *args, **kwargs):
        response = super(TagListViewSet, self).list(request, *args, **kwargs)
        response.template_name = 'tag/tag_list.html'

        queryset = self.filter_queryset(self.get_queryset())
        response.data['all'] = queryset.count()

        return response


class TagViewSet(mixins.UpdateModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]
    queryset = Tag.objects.all()


tag_list = TagListViewSet.as_view({'get': 'list'})
tag_part_update = TagViewSet.as_view({'patch': 'partial_update'})
tag_create = TagViewSet.as_view({'post': 'create'})
tag_delete = TagViewSet.as_view({'delete': 'destroy'})
