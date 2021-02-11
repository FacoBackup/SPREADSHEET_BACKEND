from django.contrib import admin
from django.urls import path
from src.user import views as user_views
from src.group import views as group_views
from src.file_management import views as file_management_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # USER
    path('api/update/profile', user_views.update_profile, name='update_profile'),
    #BUGGED
    path('api/search/user', user_views.search_user, name="search_user"),
    path('api/user', user_views.create_user, name="create_user"),
    path('api/get/user/by_id', user_views.get_user_by_id, name="get_user_by_id"),
    path('api/get/users', user_views.get_users, name="get_users"),
    path('api/get/users/by_max_id', user_views.get_user_by_max_id, name="get_users_by_max_id"),
    path('api/sign_in', user_views.sign_in, name="sign_in"),
    # USER

    # GROUP
    path('api/group', group_views.create_group, name="create_group"),
    path('api/get/group', group_views.get_group, name="get_group"),
    path('api/get/group/members', group_views.get_group_members, name='get_group_members'),
    path('api/search/group', group_views.search_group, name='search_group'),
    # GROUP

    # REPOSITORY
    path('api/get/branch', file_management_views.read_branch, name="read_branch"),
    path('api/get/repository', file_management_views.get_repository, name="read_repository"),
    path('api/get/repository/branches', file_management_views.read_repository_branches, name="read_repository_branches"),
    path('api/member/by/branch', file_management_views.verify_member_by_branch, name="verify_member_by_branch"),
    path('api/make/commit', file_management_views.make_commit, name='make_commit'),
    path('api/get/branch/contributors', file_management_views.read_branch_contributors, name="branch_contributors"),
    path('api/user/branches', file_management_views.read_contributor_branches, name='get_user_branches'),
    #TODO FONTEND
    path('api/add/contributor', file_management_views.add_contributor, name='add_contributor'),
    path('api/remove/contributor', file_management_views.remove_contributor, name='remove_contributor'),
    path('api/get/latest/commits', file_management_views.read_latest_commits, name="get_latest_commits"),
    path('api/repository', file_management_views.create_repository, name="create_repository"),
    path('api/branch', file_management_views.create_branch, name="create_branch"),
    path('api/merge', file_management_views.merge_branches, name="merge_branches"),
    #TODO FONTEND
    path('api/group/repositories', file_management_views.read_group_repositories, name="read_group_repositories"),
    #TODO FONTEND
    path('api/get/branch/commits', file_management_views.read_branch_commits, name="read_branch_commits"),
    # REPOSITORY

    # FORM
    #TODO
    path('api/export', file_management_views.export_formatted_json, name='export_formatted_json'),
    path('api/branch/update/column', file_management_views.update_column, name="update_column"),
    path('api/branch/column', file_management_views.create_column, name="create_column"),
    path('api/branch/cell', file_management_views.create_cell, name="create_cell"),
    path('api/branch/delete/cell', file_management_views.delete_cell, name="delete_cell"),
    path('api/branch/update/cell', file_management_views.update_cell, name="update_cell"),
    path('api/get/branch/content', file_management_views.read_all_content_by_branch, name="get_all_content"),
    # FORM
]
