from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('post-item/', views.post_item, name='post_item'),
]