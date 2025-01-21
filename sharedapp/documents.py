
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from tenant_app.models import BlogPost
from django.utils.text import slugify

@registry.register_document
class BlogPostDocument(Document):
    category = fields.TextField(attr='category.name')

    class Django:
        model = BlogPost
        fields = [
            'title',
            'content',
            'created_at',
        ]

    class Index:
        name = 'blogs'  # Base name, but adjusted per tenant

    @classmethod
    def for_tenant(cls, tenant_name):
        """Return an instance of BlogPostDocument with a dynamic index name for a given tenant."""
        instance = cls()
        instance._index._name = f"{slugify(tenant_name)}_blogs"
        return instance