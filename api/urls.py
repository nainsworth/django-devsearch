from django.urls import path
from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # Tokens
    path("users/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("users/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # Pages
    path("", views.getRoutes),
    path("projects/", views.getProjects),
    path("projects/<str:pk>/", views.getProject),
    path("projects/<str:pk>/vote/", views.projectVote),
]
