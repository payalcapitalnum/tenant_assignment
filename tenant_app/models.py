from django.db import models
from django.contrib.auth.models import User

from django.db import connection  # To get the current tenant schema
from elasticsearch import Elasticsearch, NotFoundError
from django.conf import settings

es = Elasticsearch(settings.ELASTICSEARCH_DSL['default']['hosts'])

class TenantSpecificModel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def _str_(self):
        return self.name



class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey('sharedapp.BlogCategory', on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts',default=1)  # Add this field

    def _str_(self):
        return self.title


class BlogComment(models.Model):
    post = models.ForeignKey(BlogPost, related_name='comments', on_delete=models.CASCADE)
    author = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f'Comment by {self.author} on {self.post.title}'


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f'Notification for {self.user.username}'