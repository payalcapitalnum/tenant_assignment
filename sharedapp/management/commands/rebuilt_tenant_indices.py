from django.core.management.base import BaseCommand
from django.core.management import call_command
from django_tenants.utils import schema_context
from tenant_app.models import BlogPost
from myapp.models import Client  # Adjust to your Client model location

class Command(BaseCommand):
    help = 'Rebuild Elasticsearch indices for all tenants'

    def handle(self, *args, **kwargs):
        # Fetch all tenant clients
        tenants = Client.objects.all()
        for tenant in tenants:
            self.stdout.write(f"================> {tenant.name}")
            self.stdout.write(f"Processing tenant: {tenant.name}")

            # Skip the public schema as it does not contain tenant-specific tables
            if tenant.schema_name == 'public':
                self.stdout.write("Skipping public schema.")
                continue

            # Activate the schema for the current tenant
            with schema_context(tenant.schema_name):
                self.stdout.write(f"Switched to schema: {tenant.schema_name}")

                try:
                    # Fetch all BlogPost instances for the current tenant schema
                    blogposts = BlogPost.objects.all()
                    self.stdout.write(f"Number of blog posts for {tenant.schema_name}: {blogposts.count()}")

                    # Rebuild Elasticsearch index for the current tenant
                    self.stdout.write(f"Rebuilding Elasticsearch index for tenant: {tenant.schema_name}")
                    call_command('search_index', '--rebuild', '--noinput')
                    self.stdout.write(f"Successfully rebuilt index for tenant: {tenant.schema_name}")

                except Exception as e:
                    self.stdout.write(f"Error processing {tenant.schema_name}: {str(e)}")






# # tenant_app/management/commands/index_blog_posts.py
#
# from django.core.management.base import BaseCommand
# from django_tenants.utils import schema_context
# from tenant_app.models import BlogPost
# from tenant_app.documents import BlogPostDocument
# from django.contrib.auth.models import User
# from myapp.models import Client
#
# class Command(BaseCommand):
#     help = 'Index blog posts for each tenant and perform a search'
#
#     def handle(self, *args, **kwargs):
#         user = User.objects.first()  # Adjust this to select a specific user
#         if not user:
#             self.stdout.write(self.style.ERROR('No user found'))
#             return
#
#         tenants = Client.objects.all()
#
#         for tenant in tenants:
#             self.stdout.write(f"Processing tenant: {tenant.schema_name}")
#
#             with schema_context(tenant.schema_name):
#                 # Create a blog post for the tenant
#                 blog_post = BlogPost.objects.create(
#                     title="My First Blog Post",
#                     content="This is the content.",
#                     author=user
#                 )
#                 blog_post.index_blog_post()
#
#                 # Search within the tenant
#                 search = BlogPostDocument.search().query("multi_match", query="First Blog", fields=["title", "content"])
#                 results = search.execute()
#                 self.stdout.write(f"Results for {tenant.schema_name}: {results}")
#
#         self.stdout.write(self.style.SUCCESS('Indexing and search complete'))

# tenant_app/management/commands/rebuild_tenant_indices.py

