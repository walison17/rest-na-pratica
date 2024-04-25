from django.contrib.admin.apps import AdminConfig


class DefaultTenantAdminConfig(AdminConfig):
    default_site = "devpro.core.admin.DefaultTenantAdminSite"
