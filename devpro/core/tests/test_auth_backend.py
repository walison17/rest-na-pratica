import pytest
from django.contrib.auth.models import User

from devpro.core.auth_backends import TenantModelBackend
from devpro.core.models import Library, UserProfile


@pytest.mark.django_db
def test_tenant_model_backend(rf):
    backend = TenantModelBackend()

    tenant = Library.objects.create(name="Saraiva", slug="saraiva")
    user = User.objects.create_user(
        username="123",
        email="walison@devpro.com.br",
        password="12345",
    )
    UserProfile.objects.create(user=user, library=tenant)

    request = rf.get("/login", headers={"host": "saraiva.devpro.example"})
    request.tenant = tenant

    assert backend.authenticate(request, "walison@devpro.com.br", "12345") == user
