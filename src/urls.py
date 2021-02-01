"""AEB_REST_API2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
from src.user import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/test', views.test, name="test"),
    path('api/user', views.create_user, name="create_user"),
    path('api/get/user/by_id', views.get_user_by_id, name="get_user"),
    path('api/get/users', views.get_users, name="get_users"),
    path('api/get/users/by_max_id', views.get_user_by_max_id, name="get_users_by_max_id")
]
