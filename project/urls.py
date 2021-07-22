"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenObtainPairView,
)

from users.views import signup_view, user_detail_view
from posts.views import PostViewSet


router = DefaultRouter()
router.register(r"posts", PostViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("signup/", signup_view, name="signup"),
    path("user/<int:pk>/", user_detail_view, name="user-detail"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/obtain/", TokenObtainPairView.as_view(), name="token_obtain"),
    path("", include(router.urls)),
]
