from datetime import date

from django import forms
from django.core import validators

from .models import Author, Book


def year_validator(value):
    today = date.today()
    if value > today.year:
        raise forms.ValidationError(
            "Não é possível cadastrar um livro que ainda não foi publicado"
        )


class BookForm(forms.Form):
    name = forms.CharField(label="Nome")
    edition = forms.IntegerField(label="Edição", initial=1, validators=[
        validators.MinValueValidator(1, message="Edição deve ser maior ou igual a 1")
    ])
    publication_year = forms.IntegerField(label="Ano de publicação", validators=[year_validator])

    def clean_name(self):
        name = self.cleaned_data["name"]
        return name.title()


class BookModelForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["name", "edition", "publication_year"]

    def clean_name(self):
        name = self.cleaned_data["name"]
        return name.title()


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ["name"]
