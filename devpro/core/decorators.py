import functools

from django.http import Http404

from devpro.core.tenant import is_default_tenant


def default_tenant(view):
    @functools.wraps(view)
    def wrapper(request, *args, **kwargs):
        if not is_default_tenant(request.tenant):
            raise Http404()

        return view(request, *args, **kwargs)

    return wrapper
