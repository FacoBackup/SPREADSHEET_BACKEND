from rest_framework import status
from django.core import exceptions
from src.file_management.models import Branch, Column, Cell
import time
from src.file_management.models import Commit


class FormFactory:
    @staticmethod
    def create_column(branch_id, name):
        try:
            column = Column(name=name, branch_fk=Branch.objects.get(id=branch_id))
            column.save()

            return status.HTTP_201_CREATED
        except exceptions.FieldError:
            return status.HTTP_500_INTERNAL_SERVER_ERROR
        except exceptions.PermissionDenied:
            return status.HTTP_500_INTERNAL_SERVER_ERROR

    @staticmethod
    def create_cell(content, column_id, user_id, row):
        try:

            column = Column.objects.get(id=column_id)
            if column is not None:
                cell = Cell(content=content, column_fk=column, row=row)
                cell.save()
                open_commit = Commit.objects.get(closed=False,
                                                 user_fk=user_id,
                                                 branch_fk=column.branch_fk.id)
                if open_commit is not None:
                    open_commit.changes += 1
                    open_commit.commit_time = time.time()
                    open_commit.save()
            return status.HTTP_201_CREATED
        except exceptions.FieldError:
            return status.HTTP_500_INTERNAL_SERVER_ERROR
        except exceptions.PermissionDenied:
            return status.HTTP_500_INTERNAL_SERVER_ERROR
