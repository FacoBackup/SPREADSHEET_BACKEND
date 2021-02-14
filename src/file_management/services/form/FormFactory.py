from rest_framework import status
from django.core import exceptions
from src.file_management.models import Branch, Column, Cell
import time
from src.file_management.models import Commit
from src.file_management.services.form import FormReader
from src.file_management.services.repository import RepositoryFactory


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

                RepositoryFactory.RepositoryFactory.set_commit(user_id=user_id, branch_id=column.branch_fk.id)
            return FormReader.FormReadService.map_cell(cell)
        except exceptions.FieldError:
            return None
        except exceptions.PermissionDenied:
            return None
