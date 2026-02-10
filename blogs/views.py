from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Blog, Category
from django.db.models import Q


# Create your views here.

def posts_by_category(request, category_id):
    # fetch the posts taht belongs to the category with the id category_id
    # foreign key will always store the id
    posts = Blog.objects.filter(status='Published', category_id=category_id)
    
    # use try/except hen we want to do some customer action if the category does not exist
    try:
        category = Category.objects.get(pk=category_id)
    except:
        # redirect the user to homepage
        return redirect('home')

    # use get_object_or_404 when you wan to show 404 error page if the category does not exist
    # category =get_object_or_404(Category, pk=category_id)
    
    context = {
        'posts' : posts,
        'category' : category,
    }
    return render(request, 'posts_by_category.html', context)

def blogs(request, slug):
    single_blog = get_object_or_404(Blog, slug=slug, status='Published')
    context = {
        'single_blog' : single_blog, 
    }
    return render(request, 'blogs.html', context)

def search(request):
    keyword = request.GET.get('keyword')

    blogs = Blog.objects.filter(Q(title__icontains=keyword) | Q(short_description__icontains=keyword) | Q(blog_body__icontains=keyword), status="published", )
    print(blogs)
    context = {
        'blogs': blogs
    }
    return render(request, "search.html", context)
