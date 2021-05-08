from django.urls import path

from .views import create_post, evaluate_post, get_posts_analytics, get_likes_analysis


urlpatterns = [
    path('create/', create_post),
    path('post/evaluate/', evaluate_post),
    path('analytics/', get_posts_analytics),
    path('likes/analytics/', get_likes_analysis)
]
