from src.file_management.models import Branch, Commit, Repository, Contributor
from django.core import exceptions, serializers
from rest_framework import status
from src.user.services import UserReader
from src.group.services import GroupReader


class RepositoryReadService:
    @staticmethod
    def read_branch(branch_id):
        try:
            branch = Branch.objects.get(id=branch_id)
            if branch is not None:
                return RepositoryReadService.__map_contributor_branch(branch)
            else:
                return None
        except exceptions.ObjectDoesNotExist:
            return None

    @staticmethod
    def read_repository(repository_id):
        try:
            repository = Repository.objects.get(id=repository_id)
            if repository is not None:
                return RepositoryReadService.__map_repository(repository)
            else:
                return None
        except exceptions.ObjectDoesNotExist:
            return None

    @staticmethod
    def verify_member_by_branch(branch_id, user_id):
        try:
            branch = Branch.objects.get(id=branch_id)
            if branch is not None:
                membership = GroupReader.GroupReadService.verify_member(user_id=user_id,
                                                                        group_id=branch.repository_fk.group_fk.id)
                if membership is not None:
                    return True
                else:
                    return False
        except exceptions.ObjectDoesNotExist:
            return False

    @staticmethod
    def read_branch_contributors(branch_id):
        try:
            contributors = Contributor.objects.filter(branch_fk=branch_id)
            response = []
            for i in contributors:
                user = UserReader.UserReadService.read_user_by_id(user_id=i.user_fk.id)
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
                branch = RepositoryReadService.__map_contributor_branch(Branch.objects.get(id=i.branch_fk.id))

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
                    __map_contributor_branch(Branch.objects.get(id=i.branch_fk.id))
                if branch is not None:
                    branches.append(branch)
            return branches
        except exceptions.ObjectDoesNotExist:
            return []

    @staticmethod
    def read_latest_commits(user_id):
        try:
            commits = Commit.objects.filter(user_fk=user_id, closed=True).order_by('-commit_time')[:2]
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
                master = Branch.objects.get(repository_fk=i.id, is_master=True)
                branches = Branch.objects.filter(repository_fk=i.id).count()
                if master is not None:
                    response.append(
                        {
                            "repository": RepositoryReadService.__map_repository(i),
                            "master_branch_id": master.id,
                            "branches": branches
                        }
                    )

            return response
        except exceptions.ObjectDoesNotExist:
            return status.HTTP_500_INTERNAL_SERVER_ERROR

    @staticmethod
    def read_repository_branches(repository_id):
        try:
            branches = Branch.objects.filter(repository_fk=repository_id)
            response = []
            for i in branches:
                response.append(RepositoryReadService.__map_contributor_branch(i))

            return response
        except exceptions.ObjectDoesNotExist:
            return status.HTTP_500_INTERNAL_SERVER_ERROR

    @staticmethod
    def read_branch_commits(branch_id):
        try:
            commits = Commit.objects.filter(branch_fk=branch_id, changes__gt=0).order_by('-commit_time')
            response = []
            for i in commits:
                response.append(RepositoryReadService.__map_commit(i))

            return response
        except exceptions.ObjectDoesNotExist:
            return status.HTTP_500_INTERNAL_SERVER_ERROR

    @staticmethod
    def __map_contributor_branch(branch):
        return {
            "id": branch.id,
            "name": branch.name,
            "repository_id": branch.repository_fk.id,
            "is_master": branch.is_master,
            'repository_name': branch.repository_fk.name,

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
            'branch_name': commit.branch_fk.name,
            "user_name": commit.user_fk.name,
            'repository_id': commit.branch_fk.repository_fk.id
        }
