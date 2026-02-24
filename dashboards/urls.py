from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('categories/', views.categories, name='categories'),
    path('blogs/', views.categories, name='blogs'),
    path('logout/', views.categories, name='logout'),
    # caterogy crud
    path('categories/add/', views.add_category, name='add_category'),
    path('categories/edit/<int:pk>/', views.edit_category, name='edit_category'),
    path('categories/delete/<int:pk>/', views.delete_category, name='delete_category'),
    # blog post crud
    path('posts/', views.posts, name='posts'),
    path('posts/add/', views.add_post, name='add_post'), 
]