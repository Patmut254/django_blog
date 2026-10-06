from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db.models import F, Q
from django.utils.http import url_has_allowed_host_and_scheme
from .models import Blog, Category, Subscriber


# Create your views here.

def posts_by_category(request, category_id):
    # fetch the posts taht belongs to the category with the id category_id
    # foreign key will always store the id
    posts = Blog.objects.filter(status='Published', category_id=category_id).order_by('-created_at')

    # use try/except hen we want to do some customer action if the category does not exist
    try:
        category = Category.objects.get(pk=category_id)
    except Category.DoesNotExist:
        # redirect the user to homepage
        return redirect('home')

    # use get_object_or_404 when you wan to show 404 error page if the category does not exist
    # category =get_object_or_404(Category, pk=category_id)

    page = Paginator(posts, 9).get_page(request.GET.get('page'))
    context = {
        'posts' : page,
        'lead_post': posts.first() if page.number == 1 else None,
        'category' : category,
        'post_count': posts.count(),
    }
    return render(request, 'posts_by_category.html', context)

def all_posts(request):
    posts = Blog.objects.filter(status='Published').select_related('category', 'author').order_by('-created_at')
    page = Paginator(posts, 12).get_page(request.GET.get('page'))
    return render(request, 'all_posts.html', {'posts': page})

def blogs(request, slug):
    single_blog = get_object_or_404(Blog, slug=slug, status='Published')

    # count the view without touching updated_at
    Blog.objects.filter(pk=single_blog.pk).update(views=F('views') + 1)

    published = Blog.objects.filter(status='Published')
    related = published.filter(category=single_blog.category).exclude(pk=single_blog.pk).order_by('-created_at')[:4]
    context = {
        'single_blog' : single_blog,
        'related_posts': related,
        'prev_post': published.filter(created_at__lt=single_blog.created_at).order_by('-created_at').first(),
        'next_post': published.filter(created_at__gt=single_blog.created_at).order_by('created_at').first(),
        'share_url': request.build_absolute_uri(),
    }
    return render(request, 'blogs.html', context)

def search(request):
    keyword = request.GET.get('keyword', '').strip()

    blogs = Blog.objects.none()
    if keyword:
        blogs = Blog.objects.filter(Q(title__icontains=keyword) | Q(short_description__icontains=keyword) | Q(blog_body__icontains=keyword) | Q(category__category_name__icontains=keyword), status="Published", ).order_by('-created_at')
    context = {
        'blogs': blogs,
        'keyword': keyword,
    }
    return render(request, "search.html", context)

def subscribe(request):
    next_url = request.META.get('HTTP_REFERER', '/')
    if not url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        next_url = '/'

    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, 'Please enter a valid email address.')
        else:
            _, created = Subscriber.objects.get_or_create(email=email)
            if created:
                messages.success(request, "You're subscribed! Watch your inbox for our next newsletter.")
            else:
                messages.info(request, 'That email is already subscribed.')
    return redirect(next_url)
