from django.contrib import admin
from django.urls import path
from src.user import views as user_views
from src.group import views as group_views
from src.file_management.views import (RepositoryViews,
                                       CellViews,
                                       ContributorViews,
                                       ColumnViews,
                                       BranchViews,
                                       CommitViews)

urlpatterns = [
    path('admin/', admin.site.urls),

    # USER
    path('api/user/by_email', user_views.get_user_by_email, name="get_user_by_email"),
    path('api/get/users', user_views.get_users, name="get_users"),
    path('api/update/profile', user_views.update_profile, name='update_profile'),
    path('api/search/user', user_views.search_user, name="search_user"),
    path('api/search/user/backward', user_views.search_user_backward, name="search_user_backward"),
    path('api/user', user_views.create_user, name="create_user"),
    path('api/get/user/by_id', user_views.get_user_by_id, name="get_user_by_id"),
    path('api/sign_in', user_views.sign_in, name="sign_in"),
    # USER

    # GROUP
    path('api/group', group_views.create_group, name="create_group"),
    path('api/get/group', group_views.get_group, name="get_group"),
    path('api/get/group/members', group_views.get_group_members, name='get_group_members'),
    path('api/search/group', group_views.search_group, name='search_group'),
    path('api/search/group/backward', group_views.search_group_backward, name='search_group_backward'),
    # GROUP


    # BRANCH
    path('api/branch', BranchViews.read_branch, name="read_branch"),
    path('api/get/repository/branches', BranchViews.read_repository_branches, name="read_repository_branches"),
    path('api/member/by/branch', BranchViews.verify_member_by_branch, name="verify_member_by_branch"),
    path('api/branch/contributors', BranchViews.read_branch_contributors, name="branch_contributors"),
    path('api/user/branches', BranchViews.read_contributor_branches, name='get_user_branches'),
    path('api/branch', BranchViews.create_branch, name="create_branch"),
    path('api/search/branch', BranchViews.search_branch, name="search_branch"),
    path('api/search/branch/backward', BranchViews.search_branch_backwards, name="search_branch_backwards"),
    path('api/merge', BranchViews.merge_branches, name="merge_branches"),
    path('api/verify/branch/name', BranchViews.verify_branch_name, name='verify_branch_name'),
    path('api/branch/content', BranchViews.read_all_content_by_branch, name="get_all_content"),
    path('api/export', BranchViews.export_formatted_json, name='export_formatted_json'),
    path('api/check/access/to/branch', BranchViews.check_access, name="check_access"),
    # BRANCH

    # CONTRIBUTOR
    path('api/add/contributor', ContributorViews.add_contributor, name='add_contributor'),
    path('api/remove/contributor', ContributorViews.remove_contributor, name='remove_contributor'),
    # CONTRIBUTOR

    # REPOSITORY
    path('api/repository', RepositoryViews.get_repository, name="read_repository"),
    path('api/create/repository', RepositoryViews.create_repository, name="create_repository"),
    path('api/group/repositories', RepositoryViews.read_group_repositories, name="read_group_repositories"),
    # REPOSITORY

    # COMMIT
    path('api/get/branch/commits', CommitViews.read_branch_commits, name="read_branch_commits"),
    path('api/make/commit', CommitViews.make_commit, name='make_commit'),
    path('api/latest/commits', CommitViews.read_latest_commits, name="get_latest_commits"),
    path('api/verify/open/commit', CommitViews.verify_open_commit, name="verify_open_commit"),
    # COMMIT

    # CELL
    path('api/branch/cell', CellViews.create_cell, name="create_cell"),
    path('api/branch/delete/cell', CellViews.delete_cell, name="delete_cell"),
    path('api/branch/update/cell', CellViews.update_cell, name="update_cell"),
    # CELL

    # COLUMN
    path('api/branch/update/column', ColumnViews.update_column, name="update_column"),
    path('api/branch/create/column', ColumnViews.create_column, name="create_column"),
    # COLUMN
]
