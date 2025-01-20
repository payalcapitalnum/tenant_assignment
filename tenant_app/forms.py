
from django import forms
from .models import TenantSpecificModel
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import BlogPost, BlogComment
from sharedapp.models import BlogCategory  

class TenantSpecificModelForm(forms.ModelForm):
    class Meta:
        model = TenantSpecificModel
        fields = ['name', 'description']


class BlogPostForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=BlogCategory.objects.all())  # Shared categories

    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'category']


class BlogCommentForm(forms.ModelForm):
    class Meta:
        model = BlogComment
        fields = ['content']



class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']