from django.template.defaultfilters import slugify

from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from tenant_app.models import BlogPost

# @registry.register_document
# class BlogPostDocument(Document):
#     # Define only fields that require custom mappings
#     category = fields.KeywordField()
#     author = fields.KeywordField()
#
#     class Index:
#         # Tenant-specific index naming can be handled dynamically if needed
#         name = 'blogpost'
#
#     class Django:
#         model = BlogPost
#         # Only include fields here that do not need custom mappings
#         fields = [
#             'title',  # Let Django Elasticsearch DSL handle basic text fields automatically
#             'content',
#             'created_at',
#         ]
#
#     def prepare_author(self, instance):
#         """Convert the author field to a username for serialization."""
#         return instance.author.username if instance.author else None
#
#     def prepare_category(self, instance):
#         """Convert the category field to a name for serialization."""
#         return instance.category.name if instance.category else None
#
#     def prepare_created_at(self, instance):
#         """Convert the created_at field to an ISO 8601 string."""
#         return instance.created_at.isoformat() if instance.created_at else None
#
#     @classmethod
#     def for_tenant(cls, tenant_name):
#         """Return an instance of BlogDocument with a dynamic index name for a given tenant."""
#         slugified_name = slugify(tenant_name)
#         instance = cls()
#         instance._index._name = f"{slugified_name}_blogs"
#         return instance

# tenant_app/documents.py
# from django.template.defaultfilters import slugify
# from django_elasticsearch_dsl import Document
# from django_elasticsearch_dsl.registries import registry
# from .models import BlogPost
#
# @registry.register_document
# class BlogPostDocument(Document):
#     class Django:
#         model = BlogPost
#         fields = [
#             "title",
#             "created_at",
#         ]
#
#     class Index:
#         # The base name for the index; it will be dynamically changed for each tenant.
#         name = "blogs"
#
#     @classmethod
#     def for_tenant(cls, tenant_name):
#         """Return an instance of BlogDocument with a dynamic index name for a given tenant."""
#         slugified_name = slugify(tenant_name)
#         instance = cls()
#         instance._index._name = f"{slugified_name}_blogs"
#         return instance

from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from tenant_app.models import BlogPost  # Adjust this import as needed

# @registry.register_document
# class BlogPostDocument(Document):
#     class Index:
#         name = 'blogs'  # This is just a base name, and you might use a method to modify it per tenant
#
#     class Django:
#         model = BlogPost
#         fields = [
#             'title',
#             'content',
#             'created_at'
#         ]
#
#     @classmethod
#     def for_tenant(cls, tenant_name):
#         """Return an instance of BlogPostDocument with a dynamic index for the given tenant."""
#         instance = cls()
#         # Slugify or adjust the tenant name for the index
#         instance._index._name = f"{slugify(tenant_name)}_blogs"
#         return instance

# from django_elasticsearch_dsl import Document
# from django_elasticsearch_dsl.registries import registry
# from tenant_app.models import BlogPost  # Adjust the import as needed
#
# @registry.register_document
# class BlogPostDocument(Document):
#     # Define how to index the category field
#     category = fields.TextField(attr='category.name')
#
#     class Django:
#         model = BlogPost
#         fields = [
#             'title',
#             'content',
#             'created_at',
#         ]
#
#     class Index:
#         name = 'blogs'  # This is the base name, and you might use a method to modify it per tenant
#
#     @classmethod
#     def for_tenant(cls, tenant_name):
#         """Return an instance of BlogPostDocument with a dynamic index name for a given tenant."""
#         instance = cls()
#         # Slugify the tenant name to ensure the index name is valid
#         instance._index._name = f"{slugify(tenant_name)}_blogs"
#         return instance

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