from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('post-item/', views.post_item, name='post_item'),
    path('profile/', views.edit_profile, name='edit_profile'),
    path('profile/<int:profile_id>/', views.view_profile, name='view_profile')
]