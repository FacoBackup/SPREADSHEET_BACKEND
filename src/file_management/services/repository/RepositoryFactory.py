from rest_framework import status
from django.core import exceptions
from src.file_management.models import Repository, Branch, Commit, Column, Cell, Contributor
from src.user.models import User
from src.group.models import Group
from src.file_management.services.form import FormFactory, FormRead
from src.group.services import GroupManagement, GroupReader
import time


class RepositoryFactory:
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
    def create_branch(repository_id, requester, name, about):
        try:
            master = Branch.objects.get(repository_fk=repository_id, is_master=True)
            columns = FormRead.FormReadService.read_columns(branch_id=master.id)
            cells = FormRead.FormReadService.read_all_cells_from_branch(branch_id=master.id)
            new_column_relations = []

            new_branch = Branch(repository_fk=repository_id, name=name, about=about, is_master=False)
            new_branch.save()

            new_contributor = Contributor(user_fk=requester, branch_fk=new_branch)
            new_contributor.save()

            for i in columns:
                new_column = Column(name=i['name'], branch_fk=new_branch.id)
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
        except exceptions.FieldError:
            return status.HTTP_500_INTERNAL_SERVER_ERROR
        except exceptions.PermissionDenied:
            return status.HTTP_500_INTERNAL_SERVER_ERROR

    # {
    #     "commit_message": "COMMIT MESSAGE",
    #     "branch_id": 19826738,
    #     "data": [
    #         {
    #             "column_id": 123,
    #             "cell_id": 1234412,
    #             "new_content": "THIS IS AN EDITED CELL"
    #         },
    #         {
    #             "column_id": 12334554,
    #             "cell_id": 1234412123,
    #             "new_content": "THIS IS AN EDITED CELL"
    #         },
    #         {
    #             "column_id": 123213,
    #             "cell_id": 1234411232,
    #             "new_content": "THIS IS AN EDITED CELL"
    #         },
    #         {
    #             "column_id": 123213,
    #             "cell_id": null,
    #             "new_content": "THIS CELL WAS CREATED NOW"
    #         }
    #     ]
    # }
    @staticmethod
    def merge(source_branch_id, target_branch_id, requester):
        try:
            target_branch = Branch.objects.get(id=target_branch_id)
            source_branch = Branch.objects.get(id=source_branch_id)

            if (target_branch is not None) and \
                    (source_branch is not None) and \
                    (target_branch.repository_fk == source_branch.repository_fk):
                repository = Repository.objects.get(id=target_branch.repository_fk)
                member = None
                if repository is not None:
                    member = GroupReader.GroupReadService.verify_member(user_id=requester, group_id=repository.group_fk)

                if member is not None:
                    columns = FormRead.FormReadService.read_columns(branch_id=source_branch_id)

                    for i in columns:
                        cells = FormRead.FormReadService.read_column_cells(column_id=i['id'])
                        column_id = FormFactory.FormFactory.create_column(name=i['name'], branch_id=target_branch_id)

                        if column_id is not None:
                            for j in cells:
                                FormFactory.FormFactory.create_cell(column_id=column_id, content=j['content'],
                                                                    requester=requester)

                    return status.HTTP_200_OK
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

    # {
    #     "branch_id": 1,
    #     "data": [
    #         {
    #             "column_id": 1,
    #             "cell_id": 1,
    #             "content": "SOME VALUE"
    #         },
    #         {
    #             "column_id": 2,
    #             "cell_id": 2,
    #             "content": null
    #         },
    #         {
    #             "column_id": 3,
    #             "cell_id": null,
    #             "content": "SOME VALUE"
    #         }
    #     ]
    # }
    # CELL_ID === NULL? CREATE CELL : EDIT CELL
    # CONTENT === NULL? DELETE CELL
    @staticmethod
    def save_changes(row):
        try:
            branch = Branch.objects.get(id=row['branch_id'])
            if branch is not None:
                for i in row['data']:
                    if i['cell_id'] is None and i['content'] is not None:
                        new_cell = Cell(column_fk=i['column_id'], content=i['content'])
                        new_cell.save()
                    elif i['content'] is None:
                        cell = Cell.objects.get(id=i['cell_id'])
                        cell.delete()
                    elif i['cell_id'] is not None and i['content'] is not None:
                        cell = Cell.objects.get(id=i['cell_id'])
                        cell.content = i['content']
                        cell.save()
        except exceptions.FieldError:
            return status.HTTP_500_INTERNAL_SERVER_ERROR
        except exceptions.PermissionDenied:
            return status.HTTP_500_INTERNAL_SERVER_ERROR
    # @staticmethod
    # def save_changes(data, requester):
    #     try:
    #         branch = Branch.objects.get(id=data['branch_id'], user_fk=requester)
    #         if branch is not None:
    #             changes = 0
    #             for i in data['data']:
    #                 if i['cell_id'] is not None and \
    #                         (i['new_content'] != "" and i['new_content'] is not None):
    #                     changes += 1
    #                     cell = Cell.objects.get(id=i['cell_id'])
    #                     cell.content = i['new_content']
    #                     cell.save()
    #                 elif i['cell_id'] is None and \
    #                         (i['new_content'] != "" and i['new_content'] is not None):
    #                     changes += 1
    #                     cell = Cell(column_fk=i['column_id'], content=i['new_content'])
    #                     cell.save()
    #
    #             RepositoryFactory.__create_commit(changes=changes,
    #                                               branch_id=data['branch_id'],
    #                                               message=data['commit_message'],
    #                                               user_id=requester
    #                                               )
    #
    #     except exceptions.FieldError:
    #         return status.HTTP_500_INTERNAL_SERVER_ERROR
    #     except exceptions.PermissionDenied:
    #         return status.HTTP_500_INTERNAL_SERVER_ERROR

    @staticmethod
    def create_commit(changes, branch_id, message, user_id):
        try:
            commit = Commit(message=message,
                            changes=changes,
                            branch_fk=Branch.objects.get(id=branch_id),
                            commit_time=time.time(),
                            user_fk=user_id
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
