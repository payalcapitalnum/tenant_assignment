from django.shortcuts import get_object_or_404
from .models import BlogPost, Notification
from .forms import BlogPostForm, BlogCommentForm,UserRegisterForm
from elasticsearch_dsl.query import MultiMatch


from django.shortcuts import redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

from django.contrib import messages

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.shortcuts import render
from sharedapp.documents import BlogPostDocument
import logging

logger = logging.getLogger(__name__)



def notifications(request):
    # Fetch all notifications for the logged-in user
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'tenantapp/notifications.html', {'notifications': notifications})


def search_blog_posts(request):
    """View to search for blog posts in a tenant-specific index."""
    query = request.GET.get('q', '').strip()  # Get the search query
    tenant_name = request.tenant.name  # Assuming you have access to the tenant name
    print("=================>", query)
    results = []

    if query:
        try:
            # Get the tenant-specific document
            blog_document = BlogPostDocument.for_tenant(tenant_name)

            # Create the search query using multi_match
            search_query = MultiMatch(query=query, fields=["title", "content"])
            search = blog_document.search().query(search_query)
            print("=======search==========>", search)

            # Execute the search query and get the hits
            response = search.execute()
            results = response.hits
            print("=============result========>", results)

            # Convert the hits to a list of dictionaries for easier rendering
            results = [
                {
                    'id': hit.meta.id,  # Ensure 'id' is included for URL generation
                    'title': hit.title,
                    'content': hit.content
                }
                for hit in results
            ]
            logger.debug(f"Search results for {tenant_name}: {results}")

        except Exception as e:
            logger.error(f"Elasticsearch search error for {tenant_name}: {str(e)}")
            results = []

    # Render the search results page with the results and the original query
    return render(request, 'tenantapp/search_results.html', {
        'results': results,
        'query': query
    })



# Registration view
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in the user after registration
            messages.success(request, "Registration successful!")
            return redirect('blog_list')  # Redirect to the blog list after registration
    else:
        form = UserRegisterForm()
    return render(request, 'tenantapp/register.html', {'form': form})

# Login view
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome {user.username}!")
                return redirect('blog_list')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'tenantapp/login.html', {'form': form})

# Logout view
@login_required
def user_logout(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('user_login')


def blog_list(request):
    posts = BlogPost.objects.all()
    return render(request, 'tenantapp/blog_list.html', {'posts': posts})


@login_required  # Ensure the user is logged in before commenting
def blog_detail(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)  # Retrieve the blog post by ID

    if request.method == 'POST':
        form = BlogCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user  # Save the request user as the comment author
            comment.save()

            # Debugging print statement to ensure this part of the code is reached
            print(f"=== User {request.user.username} commented on post {post.title}")

            # Send a notification to the post author if they are not the same as the commenter
            if post.author != request.user:
                send_notification(
                    post.author,
                    f"{request.user.username} commented: '{comment.content}' on your post '{post.title}'."
                )
                print(f"=== Notification sent to {post.author.username}")

            messages.success(request, "Your comment has been posted.")
            return redirect('blog_detail', post_id=post.id)

    else:
        form = BlogCommentForm()  # Provide an empty form for GET requests

    return render(request, 'tenantapp/blog_detail.html', {'post': post, 'form': form})



def send_notification(user, message):
    logger.info(f"Preparing to send notification to user {user.username}: {message}")

    channel_layer = get_channel_layer()
    group_name = f'user_{user.id}'

    # Log the channel layer and group name details
    logger.info(f"Using channel layer: {channel_layer}, targeting group: {group_name}")

    # Send the message to the user's WebSocket group
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': 'send_notification',
            'message': message,
        }
    )
    logger.info(f"Notification sent to group: {group_name} for user {user.username}")




@login_required
def create_blog_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            blog_post = form.save()
            tenant_name = request.tenant.name  # Adjust based on your tenant access
            # Index the blog post into the tenant-specific index
            BlogPostDocument.for_tenant(tenant_name).update(blog_post)
            logger.info("Blog post created and indexed successfully.")
            return redirect('blog_list')
    else:
        form = BlogPostForm()

    logger.debug("Rendering the blog post creation form.")
    return render(request, 'tenantapp/create_blog_post.html', {'form': form})
