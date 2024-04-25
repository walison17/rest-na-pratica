from django.http import HttpResponseNotFound

from devpro.core.tenant import (TenantDoesNotExist,
                                identify_tenant, tenant_context)


class CurrentTenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            tenant = identify_tenant(request)
        except TenantDoesNotExist:
            return HttpResponseNotFound()

        request.tenant = tenant
        with tenant_context(tenant):
            return self.get_response(request)
