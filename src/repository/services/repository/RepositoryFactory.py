from rest_framework import status
from django.core import exceptions
from src.repository.models import Repository, Branch, Commit, Column, Row
from src.user.models import User
from src.group.models import Group
from src.repository.services.form import FormFactory, FormRead
import time


class RepositoryFactory:
    @staticmethod
    def create_repository(requester, name, about, group_id):
        try:
            repository = Repository(group_fk=Group.objects.only("id").get(id=group_id), name=name, about=about)
            repository.save()
            branch = Branch(name="MASTER", is_master=True, repository_fk=repository,
                            user_fk=User.objects.only("id").get(id=requester))
            branch.save()
            return status.HTTP_201_CREATED
        except exceptions.FieldError:
            return status.HTTP_500_INTERNAL_SERVER_ERROR
        except exceptions.PermissionDenied:
            return status.HTTP_500_INTERNAL_SERVER_ERROR

    @staticmethod
    def create_branch(repository_id, requester, name, about):
        try:
            master = Branch.objects.get(repository_fk=repository_id, is_master=True)
            columns = FormRead.FormReadService.read_columns(branch_id=master.id)
            rows = FormRead.FormReadService.read_all_rows_from_branch(branch_id=master.id)
            new_column_relations = []

            new_branch = Branch(repository_fk=repository_id, name=name, about=about, user_fk=requester, is_master=False)
            new_branch.save()

            for i in columns:
                new_column = Column(name=columns[i]['name'], branch_fk=new_branch.id)
                new_column.save()
                new_column_relations.__iadd__({
                    "origin_column": columns[i]["id"],
                    "new_column": new_column.id
                })

            for j in rows:
                new_column_id = RepositoryFactory.__filter_new_column_id(old_id=rows[j]['column_id'],column_relations=new_column_relations)
                if new_column_id is not None:
                    new_row = Row(content=rows[j]['content'], column_fk=new_column_id)
                    new_row.save()

            return status.HTTP_201_CREATED
        except exceptions.FieldError:
            return status.HTTP_500_INTERNAL_SERVER_ERROR
        except exceptions.PermissionDenied:
            return status.HTTP_500_INTERNAL_SERVER_ERROR


    @staticmethod
    def save_changes(branch_id, columns, rows, commit_message, requester):
        try:

        except exceptions.FieldError:
            return status.HTTP_500_INTERNAL_SERVER_ERROR
        except exceptions.PermissionDenied:
            return status.HTTP_500_INTERNAL_SERVER_ERROR

    @staticmethod
    def create_commit(columns, rows, branch_id, message):
        try:
            old_columns = FormRead.FormReadService.read_columns(branch_id=branch_id)
            old_rows = FormRead.FormReadService.read_all_rows_from_branch(branch_id)
            columns.sort(key=RepositoryFactory.__extract_id)
            rows.sort(key=RepositoryFactory.__extract_id)
            changes = 0

            for i in columns:
                if i < len(old_columns) and old_columns[i] != columns[i]:
                    changes += 1

                elif i > len(old_columns):
                    changes += 1

            for j in rows:
                if j < len(old_rows) and old_rows[j] != rows[j]:
                    changes += 1

                elif j > len(old_rows):
                    changes += 1

            commit = Commit(message=message,
                            changes=changes,
                            branch_fk=Branch.objects.only("id").get(id=branch_id),
                            commit_time=time.time())
            commit.save()
            return status.HTTP_201_CREATED
        except exceptions.FieldError:
            return status.HTTP_500_INTERNAL_SERVER_ERROR
        except exceptions.PermissionDenied:
            return status.HTTP_500_INTERNAL_SERVER_ERROR

    @staticmethod
    def __filter_new_column_id(old_id, column_relations):
        for i in column_relations:
            if column_relations[i]['origin_column'] == old_id:
                return column_relations[i]['new_column']

        return None

    @staticmethod
    def __extract_id(json):
        try:

            return json['id']
        except KeyError:
            return 0