from contextvars import ContextVar
from contextlib import contextmanager
from dataclasses import dataclass

_tenant_state = ContextVar("current_tenant", default=None)


@contextmanager
def tenant_context(tenant):
    token = _tenant_state.set(tenant)
    try:
        yield
    finally:
        _tenant_state.reset(token)


def get_current_tenant():
    return _tenant_state.get()


def identify_tenant_by_subdomain(request):
    from devpro.core.models import Library

    subdomain = subdomain_from_request(request)
    if not subdomain:
        return False, None

    return True, Library.objects.filter(slug=subdomain).first()


def identify_tenant_by_header(request):
    from devpro.core.models import Library

    tenant_id = request.headers.get("X-Tenant-ID")
    if not tenant_id:
        return False, None

    return True, Library.objects.filter(id=tenant_id).first()


@dataclass(frozen=True)
class DefaultTenant:
    name: str
    slug: str
    pk: int = -1


_default_tenant = DefaultTenant(name='default', slug=None)


finders = [
    identify_tenant_by_subdomain,
    identify_tenant_by_header,
]


def register_finder(finder):
    finders.append(finder)


def identify_tenant(request):
    finder_applied = False

    for finder in finders:
        applied, tenant = finder(request)
        if tenant:
            return tenant

        if applied:
            finder_applied = True

    if not finder_applied:
        return _default_tenant

    raise TenantDoesNotExist(
        "Não foi possível identificar o tenant a partir da requisição"
    )


def subdomain_from_request(request):
    host = request.get_host()
    try:
        subdomain, _ = host.split(".", maxsplit=1)
    except ValueError:
        return

    return subdomain


class TenantDoesNotExist(Exception):
    pass


def is_default_tenant(tenant):
    return tenant is _default_tenant
