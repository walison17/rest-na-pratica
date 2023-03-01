from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        return Response({
            'data': data,
            'count': self.page.paginator.count,
            'current_page': self.page.number,
            'num_pages': self.page.paginator.num_pages
        })
