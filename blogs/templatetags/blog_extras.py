import re

from django import template
from django.utils.timesince import timesince

register = template.Library()

SOCIAL_ICONS = {
    'github': 'fa-github',
    'linke': 'fa-linkedin',
    'whatsapp': 'fa-whatsapp',
    'twitter': 'fa-twitter',
    'facebook': 'fa-facebook',
    'instagram': 'fa-instagram',
    'youtube': 'fa-youtube-play',
    'tiktok': 'fa-music',
}


@register.filter
def social_icon(platform):
    name = platform.lower()
    for key, icon in SOCIAL_ICONS.items():
        if key in name:
            return icon
    return 'fa-globe'


@register.filter
def resize(url, width):
    """Ask Unsplash for a smaller copy; other urls are returned unchanged."""
    if not width or 'images.unsplash.com' not in url:
        return url
    return re.sub(r'([?&])w=\d+', rf'\g<1>w={width}', url)


@register.filter
def ago(value):
    """'3 hours ago' instead of '3 hours, 12 minutes ago'."""
    return f'{timesince(value, depth=1)} ago'
