from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import obtain_token, user_create


urlpatterns = [
    path('token/', obtain_token),
    path('register/', user_create),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
