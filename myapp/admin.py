
from django.contrib import admin
from django_tenants.admin import TenantAdminMixin
from django.db import connection  # Use the connection object to get current schema
from django_tenants.utils import get_public_schema_name
from .models import Client, Domain






def is_global_superuser(request):
    """Check if the current user is a global superuser and in the public schema."""
    current_schema = connection.schema_name
    return request.user.is_superuser and current_schema == get_public_schema_name()

@admin.register(Client)
class ClientAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'schema_name', 'created_on')

    def get_queryset(self, request):
        # Only allow global superusers to see clients in the public schema
        if is_global_superuser(request):
            return super().get_queryset(request)
        return Client.objects.none()  # Tenant admins should not see any clients

    def has_module_permission(self, request):
        # Only global superusers can access the Client model
        return is_global_superuser(request)

    def has_view_permission(self, request, obj=None):
        # Only global superusers can view Client details
        return is_global_superuser(request)


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ('domain', 'tenant', 'is_primary')

    def get_queryset(self, request):
        # Only allow global superusers to see domains in the public schema
        if is_global_superuser(request):
            return super().get_queryset(request)
        return Domain.objects.none()  # Tenant admins should not see any domains

    def has_module_permission(self, request):
        # Only global superusers can access the Domain model
        return is_global_superuser(request)

    def has_view_permission(self, request, obj=None):
        # Only global superusers can view Domain details
        return is_global_superuser(request)