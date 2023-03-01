import argparse
import csv

from django.core.management.base import BaseCommand
from django.db import IntegrityError

from devpro.core.models import Author, Book


class Command(BaseCommand):
    help = 'Importa livros a partir de um csv'

    def add_arguments(self, parser):
        parser.add_argument('csv', type=argparse.FileType('r'))

    def handle(self, *args, **options):
        with options['csv'] as csvfile:
            reader = csv.DictReader(csvfile)

            count = 0
            for row in reader:
                author_names = row['authors'].split(', ')
                authors = []
                for name in author_names:
                    author, _ = Author.objects.get_or_create(name=name)
                    authors.append(author)

                try:
                    book = Book.objects.create(
                        name=row['original_title'],
                        edition=1,
                        publication_year=int(
                            float(row['original_publication_year'])
                        ),
                    )
                except IntegrityError:
                    continue
                else:
                    book.authors.set(authors)
                    count += 1

        self.stdout.write(f'{count} livros importados.')
