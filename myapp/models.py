from django_tenants.models import TenantMixin, DomainMixin
from django.db import models

class Client(TenantMixin):
    name = models.CharField(max_length=100)
    created_on = models.DateField(auto_now_add=True)

    # Add any extra fields here...

    def _str_(self):
        return self.name

class Domain(DomainMixin):
    # This model will automatically link to the tenant
    pass