from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('categories/', views.categories, name='categories'),
    path('blogs/', views.categories, name='blogs'),
    path('logout/', views.categories, name='logout'),
]