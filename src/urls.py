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
from src.user import views as user_views
from src.group import views as group_views
from src.file_management.views import FormViews, RepositoryViews

urlpatterns = [
    path('admin/', admin.site.urls),
    # USER
    path('api/user', user_views.UserViews.create_user, name="create_user"),
    path('api/get/user/by_id', user_views.UserViews.get_user_by_id, name="get_user"),
    path('api/get/users', user_views.UserViews.get_users, name="get_users"),
    path('api/get/users/by_max_id', user_views.UserViews.get_user_by_max_id, name="get_users_by_max_id"),
    path('api/sign_in', user_views.UserViews.sign_in, name="sign_in"),
    # USER

    # GROUP
    path('api/group', group_views.GroupViews.create_group, name="create_group"),
    path('api/get/group', group_views.GroupViews.get_group, name="get_group"),
    path('api/get/groups', group_views.GroupViews.get_groups_by_user, name="get_groups"),
    path('api/get/groups/by_max_id', group_views.GroupViews.get_groups_by_user_max_id, name="get_groups_by_max_id"),
    # GROUP

    # REPOSITORY
    path('api/file_management', RepositoryViews.create_repository, name="create_repository"),
    path('api/branch', RepositoryViews.create_branch, name="create_branch"),
    path('api/file_management/branches', RepositoryViews.read_repository_branches, name="read_repository_branches"),
    path('api/group/repositories', RepositoryViews.read_group_repositories, name="read_group_repositories"),
    path('api/get/branch/commits', RepositoryViews.read_branch_commits, name="read_branch_commits"),
    # REPOSITORY

    # FORM
    path('api/branch/column', FormViews.create_column, name="create_column"),
    path('api/branch/cell', FormViews.create_cell, name="create_cell"),
    path('api/get/branch/columns', FormViews.read_all_columns, name="get_all_columns"),
    path('api/get/branch/content', FormViews.read_all_content_by_branch, name="get_all_content"),
    path('api/get/cells/column', FormViews.read_all_cells_by_column, name="get_cells_by_column"),
    # FORM
]
