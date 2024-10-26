from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib import messages
from .models import User, Post, Comment 
from django.http import HttpResponse
from django.views import View
from .forms import CustomLoginForm, PostForm
from django.contrib.auth import logout
from .forms import RegistrationForm

@login_required
def home(request):
    """Render the home page with a list of posts."""
    posts = Post.objects.all() 
    return render(request, 'pages/home.html', {'posts': posts})

class LoginView(View):
    def get(self, request):
        form = CustomLoginForm()
        return render(request, 'pages/login.html', {'form': form})

    def post(self, request):
        form = CustomLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('home')  
        else:
            messages.error(request, 'Invalid username or password.')
        return render(request, 'pages/login.html', {'form': form})

# 4th flaw: A2-2017 Broken authentication:
# Login is not limiting how many login attempts you can do 
# Enabling brute-force attacks
# How to fix this:

# class LoginView(View):
#    def post(self, request):
#        form = CustomLoginForm(data=request.POST)
        
        # Rate limiting logic
#        user_ip = request.META['REMOTE_ADDR']  # Get the user's IP address
#        cache_key = f'login_attempts_{user_ip}'
#        attempts = cache.get(cache_key, 0)
#        
#        if attempts >= 5:  # Allow a maximum of 5 login attempts
#            messages.error(request, 'Too many login attempts. Please try again later.')
#            return render(request, 'pages/login.html', {'form': form})
#        
#        if form.is_valid():
#            user = form.get_user()
#            login(request, user)
#            cache.delete(cache_key)  # Reset attempts on successful login
#            messages.success(request, 'Login successful!')
#            return redirect('home')  
#        else:
#            # Increment the attempt count
#            cache.set(cache_key, attempts + 1, timeout=300)  # Timeout of 5 minutes
#            messages.error(request, 'Invalid username or password.')
#        
#        return render(request, 'pages/login.html', {'form': form})


@login_required
def profile(request):
    """Render the user's profile page."""
    return render(request, 'pages/profile.html', {'user': request.user})

@login_required
def create_post(request):
    """Handle post creation."""
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        new_post = Post.objects.create(title=title, content=content, author=request.user) 
        messages.success(request, 'Post created successfully!')
        return redirect('home')  
    return render(request, 'pages/create_post.html')

@login_required
def view_post(request, post_id):
    """View a specific post along with its comments."""
    post = get_object_or_404(Post, id=post_id)
    comments = post.comment_set.all() 
    return render(request, 'pages/view_post.html', {'post': post, 'comments': comments})

@login_required
def delete_post(request, post_id):
    """Delete a post."""
    post = get_object_or_404(Post, id=post_id)
    if request.user == post.author: 
        post.delete()
        messages.success(request, 'Post deleted successfully!')
    else:
        messages.error(request, 'You are not authorized to delete this post.')
    return redirect('home') 

@login_required
def logout_view(request):
    """Handle user logout."""
    logout(request)
    messages.success(request, 'You have been logged out successfully!')
    return redirect('login')

@login_required
def create_post(request):
    """Handle post creation."""
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = get_user_model().objects.get(id=request.user.id)
            new_post.save()
            messages.success(request, 'Post created successfully!')
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'pages/create_post.html', {'form': form})

def blog_detail(request, id):
    post = get_object_or_404(Post, id=id)
    return render(request, 'blog_detail.html', {'blog': post})

def search_blogs(request):
    search_query = request.GET.get('query', '')
    # 1st Flaw:A1:2017 - Injection: Unsanitized user input directly in database query
    posts = Post.objects.raw(f"SELECT * FROM posts WHERE title LIKE '%{search_query}%'")
    return render(request, 'pages/search_results.html', {'posts': posts})    
    # Fix: Use Django's ORM for safe queries
    # posts = Post.objects.filter(title__icontains=search_query)

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login') 
    else:
        form = RegistrationForm()

    return render(request, 'registration.html', {'form': form})

# 2nd Flaw: A3:2017 - Sensitive Data Exposure: User password is in plain text, not including hash.
# Fix: Use Django's User model which handles password hashing
# this is how user can be created safe way

# def register(request):
#    if request.method == 'POST':
#        form = RegistrationForm(request.POST)
#        if form.is_valid():
#            user = form.save(commit=False)  # Don't save yet
#            user.set_password(form.['password'])  # Hash the password
#            user.save()  # Now save the user
#            messages.success(request, 'Registration successful! You can now log in.')
#            return redirect('login')
#    else:
#        form = RegistrationForm()
#
#    return render(request, 'registration.html', {'form': form})
