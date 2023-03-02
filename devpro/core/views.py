from csv import DictWriter
import json
from http import HTTPStatus

from django.http import JsonResponse, HttpResponse, HttpResponseNotAllowed
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import resolve_url, get_object_or_404
from django.utils import timezone
from django.contrib.admin.views.decorators import staff_member_required

from devpro.core.models import Author, Book

DEFAULT_PAGE_SIZE = 25


def authors(request):
    page_number = request.GET.get('page', 1)
    page_size = request.GET.get('page_size', DEFAULT_PAGE_SIZE)

    queryset = Author.objects.all()
    if q := request.GET.get('q'):
        queryset = queryset.filter(name__icontains=q)

    paginator = Paginator(queryset, per_page=page_size)
    page = paginator.get_page(page_number)

    return JsonResponse(page2dict(page))


def book_list_create(request):
    if request.method == 'POST':
        payload = json.load(request)

        authors = payload.pop('authors')
        book = Book.objects.create(**payload)
        book.authors.set(authors)

        response = JsonResponse(book.to_dict(), status=HTTPStatus.CREATED)
        response['Location'] = resolve_url(book)
        return response
    else:
        page_number = request.GET.get('page', 1)
        page_size = request.GET.get('page_size', DEFAULT_PAGE_SIZE)

        filters = Q()
        if publication_year := request.GET.get('publication_year'):
            filters &= Q(publication_year=publication_year)

        if author_id := request.GET.get('author'):
            filters &= Q(authors=author_id)

        queryset = Book.objects.filter(filters).order_by('name')
        paginator = Paginator(queryset, per_page=page_size)
        page = paginator.get_page(page_number)

        return JsonResponse(page2dict(page))


def book_read_update_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)

    handlers = {'GET': _book_read, 'PUT': _book_update, 'DELETE': _book_delete}
    try:
        handler = handlers[request.method]
    except KeyError:
        return HttpResponseNotAllowed()

    return handler(request, book)


def _book_read(request, book):
    return JsonResponse(book.to_dict())


def _book_update(request, book):
    payload = json.load(request)
    book.name = payload['name']
    book.edition = payload['edition']
    book.publication_year = payload['publication_year']
    book.authors.set(payload['authors'])
    book.save()
    return JsonResponse(book.to_dict())


def _book_delete(request, book):
    book.delete()
    return HttpResponse(status=HTTPStatus.NO_CONTENT)


def page2dict(page):
    return {
        'data': [a.to_dict() for a in page],
        'count': page.paginator.count,
        'current_page': page.number,
        'num_pages': page.paginator.num_pages,
    }


@staff_member_required
def export_csv(request):
    books = Book.objects.prefetch_related('authors')

    if book_ids := request.GET.get('ids'):
        books = Book.objects.filter(id__in=book_ids.split(','))

    response = HttpResponse(content_type='text/csv')
    response[
        'Content-Disposition'
    ] = f'attachment; filename="books-{timezone.now():%d-%m-%Y}.csv"'
    writer = DictWriter(
        response, fieldnames=['name', 'publication_year', 'authors']
    )
    writer.writeheader()

    for book in books:
        authors = ', '.join(author.name for author in book.authors.all())
        writer.writerow(
            {
                'name': book.name,
                'publication_year': book.publication_year,
                'authors': authors,
            }
        )

    return response
