from django.db import models


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
    edition = models.PositiveIntegerField()
    publication_year = models.CharField(max_length=4)
    authors = models.ManyToManyField(Author, related_name='books')

    def __str__(self):
        return self.name
