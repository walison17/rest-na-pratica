from http import HTTPStatus

import pytest
from django.shortcuts import resolve_url

from devpro.core.models import Author

pytestmark = pytest.mark.django_db
list_authors_url = resolve_url('core:list-authors')


def test_list_all_authors(client):
    Author.objects.bulk_create(Author(name=f'Author {i}') for i in range(10))

    response = client.get(list_authors_url, data={'page': 2, 'page_size': 5})

    assert response.status_code == HTTPStatus.OK
    assert response.json()['num_pages'] == 2
    assert [a['name'] for a in response.json()['data']] == [f'Author {i}' for i in range(5, 10)]


def test_search_author_by_name(client):
    author1 = Author.objects.create(name='J.K Rowling')
    Author.objects.create(name='David Beazley')

    response = client.get(list_authors_url, data={'q': 'rowling'})

    assert response.status_code == HTTPStatus.OK
    assert response.json()['data'] == [{'id': author1.id, 'name': 'J.K Rowling'}]


def test_search_author_by_name_without_match(client):
    Author.objects.create(name='David Beazley')

    response = client.get(list_authors_url, data={'q': 'no match'})

    assert response.status_code == HTTPStatus.OK
    assert response.json()['data'] == []
