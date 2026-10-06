from .models import Category, Blog
from assignments.models import SocialLink, About

def get_categories(request):
    categories = Category.objects.all()
    return dict(categories=categories)

def get_social_links(request):
    social_links = SocialLink.objects.all()
    return dict(social_links=social_links)

def get_site_posts(request):
    # querysets are lazy, so these only hit the db on pages that use them
    published = Blog.objects.filter(status='Published').select_related('category')
    return dict(
        top_stories=published.order_by('-views', '-created_at')[:5],
        trending_post=published.order_by('-views').first,
        about=About.objects.first,
    )
