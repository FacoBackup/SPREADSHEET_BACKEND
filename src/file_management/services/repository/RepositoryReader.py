from src.file_management.models import Branch, Commit, Repository, Contributor
from django.core import exceptions, serializers
from rest_framework import status
from src.user.services.UserRead import UserReadService


class RepositoryReadService:
    @staticmethod
    def read_branch_contributors(branch_id):
        try:
            contributors = Contributor.objects.filter(branch_fk=branch_id)
            response = []
            for i in contributors:
                user = UserReadService.read_user_by_id(user_id=i.user_fk.id)
                response.append(user)

            return response
        except exceptions.ObjectDoesNotExist:
            return []

    @staticmethod
    def read_branches_user_by_max_id(user_id, max_id):
        try:
            contributor_in = (Contributor
                                  .objects
                                  .filter(user_fk=user_id, branch_fk__lt=max_id)
                                  .order_by('-branch_fk')[:10])
            branches = []

            for i in contributor_in:
                repo = Repository.objects.get(id=i.branch_fk.repository_fk)
                branch = RepositoryReadService.__map_contributor_branch(Branch.objects.get(id=i.branch_fk.id),
                                                                        repository_name=repo.name)

                if branch is not None:
                    branches.append(branch)
            return branches
        except exceptions.ObjectDoesNotExist:
            return []

    @staticmethod
    def read_branches_user(user_id):
        try:
            contributor_in = (Contributor
                                  .objects
                                  .filter(user_fk=user_id)
                                  .order_by('-branch_fk')[:10])
            branches = []

            for i in contributor_in:
                repo = Repository.objects.get(id=i.branch_fk.repository_fk)
                branch = RepositoryReadService. \
                    __map_contributor_branch(Branch.objects.get(id=i.branch_fk.id), repository_name=repo.name)
                if branch is not None:
                    branches.append(branch)
            return branches
        except exceptions.ObjectDoesNotExist:
            return []

    @staticmethod
    def read_latest_commits(user_id):
        try:
            commits = Commit.objects.filter(user_fk=user_id).order_by('-commit_time')[:3]
            response = []
            for i in commits:
                response.append(RepositoryReadService.__map_commit(i))

            return response
        except exceptions.ObjectDoesNotExist:
            return []

    @staticmethod
    def read_group_repositories(group_id):
        try:
            repositories = Repository.objects.filter(group_fk=group_id)
            response = []
            for i in repositories:
                response.append(RepositoryReadService.__map_repository(i))

            return response
        except exceptions.ObjectDoesNotExist:
            return status.HTTP_500_INTERNAL_SERVER_ERROR

    @staticmethod
    def read_repository_branches(repository_id):
        try:
            branches = Branch.objects.filter(repository_fk=repository_id)
            response = []
            for i in branches:
                response.append(RepositoryReadService.__map_repository(i))

            return response
        except exceptions.ObjectDoesNotExist:
            return status.HTTP_500_INTERNAL_SERVER_ERROR

    @staticmethod
    def read_branch_commits(branch_id):
        try:
            commits = Commit.objects.filter(branch_fk=branch_id)
            response = []
            for i in commits:
                response.append(RepositoryReadService.__map_commit(i))

            return response
        except exceptions.ObjectDoesNotExist:
            return status.HTTP_500_INTERNAL_SERVER_ERROR

    @staticmethod
    def __map_contributor_branch(branch, repository_name):
        return {
            "id": branch.id,
            "name": branch.name,
            "repository_id": branch.repository_fk.id,
            "is_master": branch.is_master,
            'repository_name': repository_name,

        }

    @staticmethod
    def __map_branch(branch):
        return {
            "id": branch.id,
            "name": branch.name,
            "repository_id": branch.repository_fk.id,
            "is_master": branch.is_master
        }

    @staticmethod
    def __map_repository(repository):
        return {
            "id": repository.id,
            "name": repository.name,
            "about": repository.about,
            "group_id": repository.group_fk.id
        }

    @staticmethod
    def __map_commit(commit):
        return {
            "id": commit.id,
            "changes": commit.changes,
            "branch_id": commit.branch_fk.id,
            "commit_time": commit.commit_time,
            "message": commit.message,
            'branch_name': commit.branch_fk.name
        }
