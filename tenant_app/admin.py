# from django.contrib import admin
# from .models import BlogPost, BlogComment


# # BlogPost admin
# class BlogPostAdmin(admin.ModelAdmin):
#     list_display = ('title', 'category', 'created_at')

#     def get_queryset(self, request):
#         """Override the default queryset to return only the tenant's data."""
#         qs = super().get_queryset(request)
#         return qs  # django-tenants will automatically limit this to the current tenant's schema


# # BlogComment admin
# class BlogCommentAdmin(admin.ModelAdmin):
#     list_display = ('post', 'author', 'content', 'created_at')

#     def get_queryset(self, request):
#         """Override the default queryset to return only the tenant's data."""
#         qs = super().get_queryset(request)
#         return qs  # This will be tenant-specific by default due to the tenant schema


# # Registering the models in the admin
# admin.site.register(BlogPost, BlogPostAdmin)
# admin.site.register(BlogComment, BlogCommentAdmin)