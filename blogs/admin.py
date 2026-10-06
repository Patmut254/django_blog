from django.contrib import admin
from .models import Category, Blog, Subscriber


class BlogAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'category', 'author', 'status', 'is_featured', 'views', 'created_at', 'updated_at')
    search_fields = ('id', 'title', 'category__category_name', 'status')
    list_editable = ('is_featured', )


class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'created_at')
    search_fields = ('email',)


admin.site.register(Category)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Subscriber, SubscriberAdmin)
