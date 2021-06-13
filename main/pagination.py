from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


# TODO docs
class BasePagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page'
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('current', self.page.number),
            ('page_range', self.page.paginator.page_range),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))
