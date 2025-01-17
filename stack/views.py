from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from stack.models import Post, Author, Subscriber
from django.http import HttpResponseForbidden

def index(request):
    posts = Post.objects.filter(published_at__isnull=False).order_by('-published_at')
    return render(request, 'index.html', {'posts': posts})

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, published_at__isnull=False)
    return render(request, 'post_detail.html', {'post': post})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Author.objects.create(user=user) # Create Author profile
            login(request, user)
            return redirect('index')  # Redirect to home after signup
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('index')

@login_required
def subscribe(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    if request.user == author.user:
        return HttpResponseForbidden("You cannot subscribe to yourself.")
    try:
        Subscriber.objects.create(user=request.user, author=author)
    except: #already subscribed
        pass
    return redirect(request.META.get('HTTP_REFERER', 'index')) # Redirect back

@login_required
def unsubscribe(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    Subscriber.objects.filter(user=request.user, author=author).delete()
    return redirect(request.META.get('HTTP_REFERER', 'index'))