import pytest
from django.http import HttpResponse

from devpro.core.middlewares import CurrentTenantMiddleware
from devpro.core.models import Author, Library
from devpro.core.tenant import (
    TenantDoesNotExist,
    get_current_tenant,
    identify_default_tenant,
    identify_tenant,
    identify_tenant_by_header,
    identify_tenant_by_subdomain,
    subdomain_from_request,
    tenant_context,
)


@pytest.fixture
def tenant_saraiva():
    return Library.objects.create(name="Saraiva", slug="saraiva")


def test_get_subdomain(rf):
    request = rf.get("/test", headers={"host": "tenant1.devpro.example:8000"})
    assert subdomain_from_request(request) == "tenant1"


@pytest.mark.django_db
def test_identify_tenant_by_subdomain(rf):
    tenant = Library.objects.create(name="Saraiva", slug="saraiva")

    request = rf.get("/test", headers={"host": "saraiva.devpro.example:8000"})

    assert identify_tenant_by_subdomain(request) == (True, tenant)


@pytest.mark.django_db
def test_current_tenant_middleware(rf):
    tenant = Library.objects.create(name="Saraiva", slug="saraiva")

    def get_response(request):
        return HttpResponse("ok")

    middleware = CurrentTenantMiddleware(get_response)

    request = rf.get("/test", headers={"host": "saraiva.devpro.example:8000"})
    middleware(request)

    assert request.tenant == tenant


@pytest.mark.django_db
def test_tenant_context(tenant_saraiva):
    with tenant_context(tenant_saraiva):
        assert get_current_tenant() == tenant_saraiva

    assert get_current_tenant() is None


@pytest.mark.django_db
def test_tenant_manager_bulk_create(tenant_saraiva):
    with tenant_context(tenant_saraiva):
        authors = Author.objects.bulk_create(
            [
                Author(name="Autor 1"),
                Author(name="Autor 2"),
            ]
        )

    for author in authors:
        assert author.library == tenant_saraiva


@pytest.mark.django_db
def test_tenant_model_save(tenant_saraiva):
    with tenant_context(tenant_saraiva):
        author = Author()
        author.name = "Monteiro Lobatto"
        author.save()

    assert author.library == tenant_saraiva


@pytest.mark.django_db
def test_identify_tenant_by_header(rf, tenant_saraiva):
    request = rf.get("/test", headers={"X-Tenant-ID": tenant_saraiva.id})

    assert identify_tenant_by_header(request) == (True, tenant_saraiva)


@pytest.mark.django_db
@pytest.mark.parametrize(
    "headers",
    [
        {"Host": "nao-existe.devpro.example"},
        {"X-Tenant-ID": 99},
    ],
)
def test_identify_tenant_not_found(rf, headers):
    request = rf.get("/test", headers=headers)

    with pytest.raises(TenantDoesNotExist):
        identify_tenant(request)


def test_identify_default_tennat(rf):
    request = rf.get("/test")

    default_tenant = identify_tenant(request)

    assert default_tenant.name == "default"
    assert default_tenant.slug is None
