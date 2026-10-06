
from django.shortcuts import render, redirect
from blogs.models import Blog, Category
from assignments.models import About
from .forms import RegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth, messages

# Create your views here.


def home(request):
    published = Blog.objects.filter(status='Published').select_related('category', 'author')
    latest = published.order_by('-created_at')
    featured_posts = list(published.filter(is_featured=True).order_by('-created_at')[:5]) or list(latest[:5])
    posts = Blog.objects.filter(is_featured=False, status='Published').order_by('-created_at')

    # every section after the hero shows posts that haven't appeared yet
    shown = {p.pk for p in featured_posts}
    rest = [p for p in latest if p.pk not in shown]

    #fetch about us
    try:
        about = About.objects.get()
    except (About.DoesNotExist, About.MultipleObjectsReturned):
        about=None

    
    context = {
        'featured_posts': featured_posts,
        'posts': posts,
        'about': about,
        'ticker_posts': latest[:4],
        'headline_posts': rest[:5],
        'dont_miss': rest[5:10],
        'editors_picks': rest[10:14],
        'latest_posts': rest[14:22],
    }
    
    return render(request, 'home.html', context)


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created. You can now log in.')
            return redirect('login')
    else:
        form = RegistrationForm()
    context ={
        'form': form,
    }
    return render(request, 'register.html', context)

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    context = {
        'form': form,
    }
    return render(request, 'login.html', context)

def logout(request):
    auth.logout(request)
    return redirect('home')