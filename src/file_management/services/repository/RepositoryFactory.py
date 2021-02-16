from rest_framework import status
from django.core import exceptions
from src.file_management.models import Repository, Branch, Commit, Column, Cell, Contributor
from src.user.models import User
from src.group.models import Group
from src.file_management.services.form import FormFactory, FormReader
from src.group.services import GroupReader
import datetime


class RepositoryFactory:

    @staticmethod
    def delete_cell(cell_id, user_id):
        try:
            cell = Cell.objects.get(id=cell_id)
            if cell is not None:
                RepositoryFactory.set_commit(user_id=user_id, branch_id=cell.column_fk.branch_fk.id)
                cell.delete()
                return status.HTTP_200_OK

            else:
                return status.HTTP_424_FAILED_DEPENDENCY
        except exceptions.FieldError:
            return status.HTTP_500_INTERNAL_SERVER_ERROR
        except exceptions.PermissionDenied:
            return status.HTTP_500_INTERNAL_SERVER_ERROR
        except exceptions.ObjectDoesNotExist:
            return status.HTTP_500_INTERNAL_SERVER_ERROR

    @staticmethod
    def update_column(column_id, user_id, name):
        try:
            column = Column.objects.get(id=column_id)
            if column is not None:
                column.name = name
                column.save()
                RepositoryFactory.set_commit(user_id=user_id, branch_id=column.branch_fk.id)
                return status.HTTP_200_OK
            else:
                return status.HTTP_424_FAILED_DEPENDENCY
        except exceptions.FieldError:
            return status.HTTP_500_INTERNAL_SERVER_ERROR
        except exceptions.PermissionDenied:
            return status.HTTP_500_INTERNAL_SERVER_ERROR
        except exceptions.ObjectDoesNotExist:
            return status.HTTP_500_INTERNAL_SERVER_ERROR

    @staticmethod
    def create_repository(requester, name, about, group_id):
        try:
            group = Group.objects.get(id=group_id)
            user = User.objects.get(id=requester)
            if user is not None and group is not None:
                repository = Repository(group_fk=group, name=name, about=about)
                repository.save()

                branch = Branch(name="MASTER", is_master=True, repository_fk=repository)
                branch.save()

                contributor = Contributor(user_fk=user, branch_fk=branch)
                contributor.save()

                return status.HTTP_201_CREATED
            else:
                return status.HTTP_424_FAILED_DEPENDENCY
        except exceptions.FieldError:
            return status.HTTP_500_INTERNAL_SERVER_ERROR
        except exceptions.PermissionDenied:
            return status.HTTP_500_INTERNAL_SERVER_ERROR

    @staticmethod
    def add_contributor_branch(branch_id, user_id, requester):
        branch = Branch.objects.get(id=branch_id)
        contributor = Contributor.objects.get(user_fk=requester, branch_fk=branch_id)
        user = User.objects.get(id=user_id)
        if branch is not None and contributor is not None and user is not None:
            new_contributor = Contributor(user_fk=user, branch_fk=branch)
            new_contributor.save()
            return status.HTTP_201_CREATED
        else:
            return status.HTTP_500_INTERNAL_SERVER_ERROR

    @staticmethod
    def remove_contributor_branch(branch_id, user_id, requester):
        contributor = Contributor.objects.get(user_fk=requester, branch_fk=branch_id)
        if contributor is not None:
            to_be_removed = Contributor.objects.get(user_fk=user_id, branch_fk=branch_id)
            to_be_removed.delete()
            return status.HTTP_200_OK
        else:
            return status.HTTP_401_UNAUTHORIZED

    @staticmethod
    def create_branch(target_branch_id, requester, name):
        try:
            target_branch = Branch.objects.get(id=target_branch_id)
            if target_branch is not None:

                new_branch = Branch(repository_fk=target_branch.repository_fk, name=name.upper(), is_master=False)
                new_branch.save()

                new_contributor = Contributor(user_fk=User.objects.get(id=requester), branch_fk=new_branch)
                new_contributor.save()

                content = FormReader.FormReadService.read_all_content_by_branch(branch_id=target_branch.id)

                for i in content:
                    new_column = Column(name=i['column_name'], branch_fk=new_branch)
                    new_column.save()

                    for j in i["cells"]:
                        new_cell = Cell(content=j["content"], row=j['row'], column_fk=new_column)
                        new_cell.save()

                return new_branch.id
            else:
                return None
        except exceptions.FieldError:
            return None
        except exceptions.PermissionDenied:
            return None


    @staticmethod
    def merge(source_branch_id, requester):
        try:
            source_branch = Branch.objects.get(id=source_branch_id)
            target_branch = Branch.objects.get(is_master=True, repository_fk=source_branch.repository_fk.id)
            old_content = Column.objects.filter(branch_fk=target_branch)
            old_content.delete()
            content = FormReader.FormReadService.read_all_content_by_branch(branch_id=source_branch.id)

            for i in content:
                new_column = Column(name=i['column_name'], branch_fk=target_branch)
                new_column.save()

                for j in i["cells"]:
                    new_cell = Cell(content=j["content"], row=j['row'], column_fk=new_column)
                    new_cell.save()
            return status.HTTP_200_OK
        except exceptions.FieldError:
            return status.HTTP_500_INTERNAL_SERVER_ERROR
        except exceptions.PermissionDenied:
            return status.HTTP_500_INTERNAL_SERVER_ERROR
        except exceptions.ObjectDoesNotExist:
            return status.HTTP_500_INTERNAL_SERVER_ERROR

    @staticmethod
    def update_cell(cell_id, user_id, content):
        try:
            cell = Cell.objects.get(id=cell_id)
            if cell is not None:
                cell.content = content
                cell.save()
                RepositoryFactory.set_commit(user_id=user_id, branch_id=cell.column_fk.branch_fk.id)
                return status.HTTP_200_OK
        except exceptions.FieldError:
            return status.HTTP_500_INTERNAL_SERVER_ERROR
        except exceptions.PermissionDenied:
            return status.HTTP_500_INTERNAL_SERVER_ERROR

    @staticmethod
    def set_commit(user_id, branch_id):
        try:
            open_commit = Commit.objects.get(closed=False,
                                             user_fk=user_id,
                                             branch_fk=branch_id)

            open_commit.changes += 1
            open_commit.commit_time = datetime.datetime.now().timestamp() * 1000
            open_commit.save()
        except exceptions.ObjectDoesNotExist:
            new_commit = Commit(closed=False,
                                user_fk=User.objects.get(id=user_id),
                                branch_fk=Branch.objects.get(id=branch_id),
                                changes=1,
                                commit_time=datetime.datetime.now().timestamp() * 1000
                                )
            new_commit.save()

    @staticmethod
    def commit(branch_id, user_id):
        try:
            last_commit = Commit.objects.get(closed=False,
                                             user_fk=user_id,
                                             branch_fk=int(branch_id))
            if last_commit is not None and last_commit.changes > 0:
                last_commit.closed = True
                last_commit.save()

                new_commit = Commit(changes=0,
                                    branch_fk=Branch.objects.get(id=branch_id),
                                    commit_time=datetime.datetime.now().timestamp() * 1000,
                                    user_fk=User.objects.get(id=user_id),
                                    closed=False
                                    )

                new_commit.save()

                return status.HTTP_201_CREATED
            else:
                return status.HTTP_424_FAILED_DEPENDENCY

        except exceptions.ObjectDoesNotExist:
            new_commit = Commit(changes=0,
                                branch_fk=Branch.objects.get(id=branch_id),
                                commit_time=datetime.datetime.now().timestamp() * 1000,
                                user_fk=User.objects.get(id=user_id),
                                closed=False
                                )
            new_commit.save()

            return status.HTTP_201_CREATED
        except exceptions.FieldError:
            return status.HTTP_500_INTERNAL_SERVER_ERROR
        except exceptions.PermissionDenied:
            return status.HTTP_500_INTERNAL_SERVER_ERROR

    @staticmethod
    def __filter_new_column_id(old_id, column_relations):
        for i in column_relations:
            if i['origin_column'] == old_id:
                return i['new_column']

        return None

    @staticmethod
    def __extract_id(json):
        try:

            return json['id']
        except KeyError:
            return 0
