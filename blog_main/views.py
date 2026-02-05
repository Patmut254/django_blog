
from django.shortcuts import render
from blogs.models import Blog, Category

# Create your views here.


def home(request):
    categories = Category.objects.all()
    context = {
        'categories': categories
    }
    return render(request, 'home.html', context)