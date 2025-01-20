from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import BlogPost, BlogComment, Notification


class BlogTestCase(TestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = Client()

        # Create a sample blog post
        self.blog_post = BlogPost.objects.create(
            title="Sample Blog Post",
            content="This is a sample blog post.",
            author=self.user
        )

    def test_register_view(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tenantapp/register.html')

    def test_login_view(self):
        response = self.client.get(reverse('user_login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tenantapp/login.html')

        # Test login functionality
        response = self.client.post(reverse('user_login'), {
            'username': 'testuser',
            'password': 'testpass'
        })
        self.assertEqual(response.status_code, 302)  # Expect a redirect after login
        self.assertRedirects(response, reverse('blog_list'))

    def test_logout_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('user_logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('user_login'))

    def test_blog_list_view(self):
        response = self.client.get(reverse('blog_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tenantapp/blog_list.html')
        self.assertContains(response, self.blog_post.title)

    def test_blog_detail_view(self):
        response = self.client.get(reverse('blog_detail', args=[self.blog_post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tenantapp/blog_detail.html')
        self.assertContains(response, self.blog_post.title)

    def test_create_blog_post_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('create_blog_post'), {
            'title': 'Test Blog',
            'content': 'Test content',
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('blog_list'))
        self.assertTrue(BlogPost.objects.filter(title='Test Blog').exists())

    def test_blog_comment_post(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('blog_detail', args=[self.blog_post.id]), {
            'content': 'This is a test comment.',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(BlogComment.objects.filter(content='This is a test comment.').exists())

    def test_notification_creation(self):
        Notification.objects.create(user=self.user, message='New notification')
        self.assertEqual(Notification.objects.count(), 1)
        self.assertEqual(Notification.objects.first().message, 'New notification')

    def test_notifications_view(self):
        self.client.login(username='testuser', password='testpass')
        Notification.objects.create(user=self.user, message='New notification')
        response = self.client.get(reverse('notifications'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tenantapp/notifications.html')
        self.assertContains(response, 'New notification')