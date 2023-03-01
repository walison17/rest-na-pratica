from django.shortcuts import resolve_url
from rest_framework import generics

from devpro.core.filters import BookFilterBackend
from devpro.core.models import Author, Book
from devpro.core.serializers import AuthorSerializer, BookSerializer


class AuthorList(generics.ListAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        if q := self.request.GET.get('q'):
            queryset = queryset.filter(name__icontains=q)

        return queryset


authors = AuthorList.as_view()


class BookListCreate(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [BookFilterBackend]

    def get_success_headers(self, data):
        headers = super().get_success_headers(data)
        headers['Location'] = resolve_url(
            'core:read-update-delete-book', pk=data['id']
        )
        return headers


book_list_create = BookListCreate.as_view()


class BookReadUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


book_read_update_delete = BookReadUpdateDelete.as_view()
