from django.urls import path

from .views import create_post, evaluate_post


urlpatterns = [
    path('create/', create_post),
    path('post/evaluate/', evaluate_post),
]
