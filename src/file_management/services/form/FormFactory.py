from rest_framework import status
from django.core import exceptions
from src.file_management.models import Branch, Column, Cell


class FormFactory:
    @staticmethod
    def create_column(branch_id, name):
        try:
            form_field = Column(name=name, branch_fk=Branch.objects.get(id=branch_id))
            form_field.save()
            return form_field.id
        except exceptions.FieldError:
            return None
        except exceptions.PermissionDenied:
            return None

    @staticmethod
    def create_cell(content, column_id, row):
        try:
            print("THIS IS THE ROW")
            print(row)
            column = Column.objects.get(id=column_id)
            if column is not None:
                cell = Cell(content=content, column_fk=column, row=row)
                cell.save()

            return status.HTTP_201_CREATED
        except exceptions.FieldError:
            return status.HTTP_500_INTERNAL_SERVER_ERROR
        except exceptions.PermissionDenied:
            return status.HTTP_500_INTERNAL_SERVER_ERROR
