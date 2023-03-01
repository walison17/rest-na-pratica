from rest_framework.filters import BaseFilterBackend
from django.db.models import Q


class BookFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        filters = Q()
        if publication_year := request.GET.get('publication_year'):
            filters &= Q(publication_year=publication_year)

        if author_id := request.GET.get('author'):
            filters &= Q(authors=author_id)

        return queryset.filter(filters)
