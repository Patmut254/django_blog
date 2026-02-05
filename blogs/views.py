from django.shortcuts import render
from django.http import HttpResponse
from .models import Blog, Category

# Create your views here.

def posts_by_category(request, category_id):
    # fetch the posts taht belongs to the category with the id category_id
    # foreign key will always store the id
    posts = Blog.objects.filter(status='Published', category_id=category_id)
    category = Category.objects.get(pk=category_id)
    context = {
        'posts' : posts,
        'category' : category,
    }
    return render(request, 'posts_by_category.html', context)