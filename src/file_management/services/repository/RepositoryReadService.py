from src.file_management.models import Branch, Commit, Repository
from django.core import exceptions, serializers
from rest_framework import status


class RepositoryReadService:
    @staticmethod
    def read_group_repositories(group_id):
        try:
            repositories = Repository.objects.filter(group_fk=group_id)
            response = []
            for i in repositories:
                response.__iadd__(RepositoryReadService.__map_repository(repositories[i]))

            return response
        except exceptions.ObjectDoesNotExist:
            return status.HTTP_500_INTERNAL_SERVER_ERROR

    @staticmethod
    def read_repository_branches(repository_id):
        try:
            branches = Branch.objects.filter(repository_fk=repository_id)
            response = []
            for i in branches:
                response.__iadd__(RepositoryReadService.__map_repository(branches[i]))

            return response
        except exceptions.ObjectDoesNotExist:
            return status.HTTP_500_INTERNAL_SERVER_ERROR

    @staticmethod
    def read_branch_commits(branch_id):
        try:
            commits = Commit.objects.filter(branch_fk=branch_id)
            response = []
            for i in commits:
                response.__iadd__(RepositoryReadService.__map_commit(commits[i]))

            return response
        except exceptions.ObjectDoesNotExist:
            return status.HTTP_500_INTERNAL_SERVER_ERROR

    @staticmethod
    def __map_branch(branch):
        return {
            "id": branch.id,
            "name": branch.name,
            "user_id": branch.user_fk,
            "repository_id": branch.repository_fk,
            "is_master": branch.is_master
        }

    @staticmethod
    def __map_repository(repository):
        return {
            "id": repository.id,
            "name": repository.name,
            "about": repository.about,
            "group_id": repository.group_fk
        }

    @staticmethod
    def __map_commit(commit):
        return {
            "id": commit.id,
            "changes": commit.changes,
            "branch_id": commit.branch_fk,
            "commit_time": commit.commit_time,
            "message": commit.message
        }