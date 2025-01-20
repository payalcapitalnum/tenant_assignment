from django.db.models.signals import post_save
from django.dispatch import receiver
from tenant_app.models import BlogPost
from sharedapp.documents import BlogPostDocument

@receiver(post_save, sender=BlogPost)
def index_blog_post(sender, instance, **kwargs):
    """Automatically index a blog post after it is saved."""
    tenant_name = instance.tenant.name  # Adjust based on how you access the tenant's name
    BlogPostDocument.for_tenant(tenant_name).update(instance)