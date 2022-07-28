from django.db import models
from django.urls import reverse


class Author(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }


class Book(models.Model):
    name = models.CharField(max_length=128)
    edition = models.PositiveSmallIntegerField()
    publication_year = models.PositiveSmallIntegerField()
    authors = models.ManyToManyField(Author, related_name='books')

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'edition': self.edition,
            'publication_year': self.publication_year,
            'authors': list(self.authors.values_list('id', flat=True))
        }

    def get_absolute_url(self):
        return reverse('core:read-update-delete-book', kwargs={'pk': self.id})
