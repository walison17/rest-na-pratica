from rest_framework import serializers

from devpro.core.models import Author, Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'name', 'edition', 'publication_year', 'authors']


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name']
