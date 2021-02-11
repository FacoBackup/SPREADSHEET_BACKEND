from rest_framework import status
from django.core import exceptions
from src.file_management.models import Repository, Branch, Commit, Column, Cell, Contributor
from src.user.models import User
from src.group.models import Group
from src.file_management.services.form import FormFactory, FormReader
from src.group.services import GroupManagement, GroupReader
import time


class RepositoryFactory:
    @staticmethod
    def delete_cell(cell_id):
        try:
            cell = Cell.objects.get(id=cell_id)
            if cell is not None:
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
    def update_column(column_id, name):
        try:
            column = Column.objects.get(id=column_id)
            if column is not None:
                column.name = name
                column.save()
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
        contributor = Contributor.object.get(user_fk=requester, branch_fk=branch_id)
        user = User.objects.get(id=user_id)
        if branch is not None and contributor is not None and user is not None:
            new_contributor = Contributor(user_fk=user, branch_fk=branch)
            new_contributor.save()
            return status.HTTP_201_CREATED
        else:
            return status.HTTP_500_INTERNAL_SERVER_ERROR

    @staticmethod
    def remove_contributor_branch(branch_id, user_id, requester):
        contributor = Contributor.object.get(user_fk=requester, branch_fk=branch_id)
        if contributor is not None:
            to_be_removed = Contributor.objects.get(user_fk=user_id, branch_fk=branch_id)
            to_be_removed.delete()
            return status.HTTP_200_OK
        else:
            return status.HTTP_401_UNAUTHORIZED

    @staticmethod
    def create_branch(target_branch_id, requester, name, about):
        try:
            target_branch = Branch.objects.get(repository_fk=target_branch_id)
            if target_branch is not None:
                columns = FormReader.FormReadService.read_columns(branch_id=target_branch.id)
                cells = FormReader.FormReadService.read_all_cells_from_branch(branch_id=target_branch.id)
                new_column_relations = []

                new_branch = Branch(repository_fk=target_branch.repository_fk, name=name, about=about, is_master=False)
                new_branch.save()

                new_contributor = Contributor(user_fk=User.objects.get(id=requester), branch_fk=new_branch)
                new_contributor.save()

                for i in columns:
                    new_column = Column(name=i['name'], branch_fk=new_branch)
                    new_column.save()
                    new_column_relations.append({
                        "origin_column": i["id"],
                        "new_column": new_column.id
                    })

                for j in cells:
                    new_column_id = RepositoryFactory.__filter_new_column_id(old_id=j['column_id'],
                                                                             column_relations=new_column_relations)
                    if new_column_id is not None:
                        new_cell = Cell(content=j['content'], column_fk=new_column_id)
                        new_cell.save()

                return status.HTTP_201_CREATED
            else:
                return status.HTTP_417_EXPECTATION_FAILED
        except exceptions.FieldError:
            return status.HTTP_500_INTERNAL_SERVER_ERROR
        except exceptions.PermissionDenied:
            return status.HTTP_500_INTERNAL_SERVER_ERROR

    @staticmethod
    def merge(source_branch_id, requester):
        try:
            source_branch = Branch.objects.get(id=source_branch_id)
            if source_branch is not None:
                target_branch = Branch.objects.get(is_master=True, repository_fk=source_branch.repository_fk.id)
                if (target_branch is not None) and \
                        (target_branch.repository_fk == source_branch.repository_fk):
                    repository = Repository.objects.get(id=target_branch.repository_fk)
                    member = None
                    if repository is not None:
                        member = GroupReader.GroupReadService.verify_member(user_id=requester,
                                                                            group_id=repository.group_fk.id)

                    if member is not None:
                        columns = FormReader.FormReadService.read_columns(branch_id=source_branch_id)

                        for i in columns:
                            cells = FormReader.FormReadService.read_column_cells(column_id=i['id'])
                            column_id = FormFactory.FormFactory.create_column(name=i['name'], branch_id=target_branch.id)

                            if column_id is not None:
                                for j in cells:
                                    FormFactory.FormFactory.create_cell(column_id=column_id, content=j['content'],
                                                                        requester=requester)

                        return status.HTTP_200_OK
                    else:
                        return status.HTTP_424_FAILED_DEPENDENCY
                else:
                    return status.HTTP_424_FAILED_DEPENDENCY
            else:
                return status.HTTP_417_EXPECTATION_FAILED
        except exceptions.FieldError:
            return status.HTTP_500_INTERNAL_SERVER_ERROR
        except exceptions.PermissionDenied:
            return status.HTTP_500_INTERNAL_SERVER_ERROR
        except exceptions.ObjectDoesNotExist:
            return status.HTTP_500_INTERNAL_SERVER_ERROR

    @staticmethod
    def update_cell(cell_id, content):
        try:
            cell = Cell.objects.get(id=cell_id)
            if cell is not None:
                cell.content = content
                cell.save()
                return status.HTTP_200_OK
        except exceptions.FieldError:
            return status.HTTP_500_INTERNAL_SERVER_ERROR
        except exceptions.PermissionDenied:
            return status.HTTP_500_INTERNAL_SERVER_ERROR

    @staticmethod
    def create_commit(changes, branch_id, message, user_id):
        try:
            commit = Commit(message=message,
                            changes=changes,
                            branch_fk=Branch.objects.get(id=branch_id),
                            commit_time=time.time(),
                            user_fk=User.objects.get(id=user_id)
                            )
            commit.save()
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
