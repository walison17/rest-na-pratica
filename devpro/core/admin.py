from functools import partial
from typing import Any
from django.contrib import admin
from django.shortcuts import redirect, resolve_url

from devpro.core.decorators import default_tenant
from devpro.core.forms import BorrowForm, CustomAdminAuthenticationForm
from devpro.core.models import Author, Book, Borrow, UserProfile
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import User, Group


class DefaultTenantAdminSite(admin.AdminSite):
    login_form = CustomAdminAuthenticationForm

    def admin_view(self, view, cacheable=False):
        view = super().admin_view(view, cacheable)
        return default_tenant(view)


admin_site = DefaultTenantAdminSite(name='default-admin')
admin_site.register([UserProfile])
admin_site.register(User, UserAdmin)
admin_site.register(Group, GroupAdmin)


register = partial(admin.register, site=admin_site)


@register(Author)
class AuthorAdmin(admin.ModelAdmin):
    search_fields = ["name"]


@register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'publication_year', 'get_authors', 'available')
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


@register(Borrow)
class BorrowAdmin(admin.ModelAdmin):
    form = BorrowForm
    list_display = ["__str__", "created_at", "returned_at"]

    def save_model(self, request: Any, obj: Any, form: Any, change: Any) -> None:
        super().save_model(request, obj, form, change)
        if obj.returned_at:
            obj.book.available = True
        else:
            obj.book.available = False
        obj.book.save()
