from rest_framework import status
from django.core import exceptions
from src.file_management.models import Repository, Branch, Commit, Column, Row
from src.user.models import User
from src.group.models import Group
from src.file_management.services.form import FormFactory, FormRead
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

    # {
    #     "commit_message": "COMMIT MESSAGE",
    #     "branch_id": 19826738,
    #     "data": [
    #         {
    #             "column_id": 123,
    #             "row_id": 1234412,
    #             "new_content": "THIS IS AN EDITED CELL"
    #         },
    #         {
    #             "column_id": 12334554,
    #             "row_id": 1234412123,
    #             "new_content": "THIS IS AN EDITED CELL"
    #         },
    #         {
    #             "column_id": 123213,
    #             "row_id": 1234411232,
    #             "new_content": "THIS IS AN EDITED CELL"
    #         },
    #         {
    #             "column_id": 123213,
    #             "row_id": null,
    #             "new_content": "THIS CELL WAS CREATED NOW"
    #         }
    #     ]
    # }
    @staticmethod
    def merge(current_branch_id, target_branch_id):
        print("TODO: not yet implemented")
        # TODO: not yet implemented

    @staticmethod
    def save_changes(data, requester):
        try:
            branch = Branch.objects.get(id=data['branch_id'], user_fk=requester)
            if branch is not None:
                changes = 0
                for i in data['data']:
                    if data[i]['row_id'] is not None and \
                            (data[i]['new_content'] != "" and data[i]['new_content'] is not None):
                        changes += 1
                        row = Row.objects.get(id=data[i]['row_id'])
                        row.content = data[i]['new_content']
                        row.save()
                    elif data[i]['row_id'] is None and \
                            (data[i]['new_content'] != "" and data[i]['new_content'] is not None):
                        changes += 1
                        row = Row(column_fk=data[i]['column_id'], content=data[i]['new_content'])
                        row.save()

                RepositoryFactory.__create_commit(changes=changes,
                                                  branch_id=data['branch_id'],
                                                  message=data['commit_message'])

        except exceptions.FieldError:
            return status.HTTP_500_INTERNAL_SERVER_ERROR
        except exceptions.PermissionDenied:
            return status.HTTP_500_INTERNAL_SERVER_ERROR

    @staticmethod
    def __create_commit(changes, branch_id, message):
        try:
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
