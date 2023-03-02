from django.contrib import admin
from django.shortcuts import redirect, resolve_url

from .models import Author, Book


admin.site.register([Author])


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'publication_year', 'get_authors')
    search_fields = ('name', 'authors__name')
    ordering = ('publication_year', 'name')
    list_filter = ('publication_year',)
    actions = ['export_csv']

    @admin.display(description='Authors')
    def get_authors(self, obj):
        return ', '.join(author.name for author in obj.authors.all())

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.prefetch_related('authors')

    @admin.action(description='Exportar como csv')
    def export_csv(self, request, queryset):
        ids = queryset.values_list('id', flat=True)
        return redirect(
            resolve_url('core:export'), ids=','.join(str(i) for i in ids)
        )
