from rest_framework import status
from django.core import exceptions
from src.repository.models import Branch, Column, Row


class FormFactory:
    @staticmethod
    def create_column(branch_id, name):
        try:
            form_field = Column(name=name, branch_fk=Branch.objects.only("id").get(id=branch_id))
            form_field.save()
            return status.HTTP_201_CREATED
        except exceptions.FieldError:
            return status.HTTP_500_INTERNAL_SERVER_ERROR
        except exceptions.PermissionDenied:
            return status.HTTP_500_INTERNAL_SERVER_ERROR

    @staticmethod
    def create_row(content, column_id, requester):
        try:
            form_content = Row(content=content,
                               creator=requester,
                               column_fk=Column.objects.only("id").get(id=column_id))
            form_content.save()
            return status.HTTP_201_CREATED
        except exceptions.FieldError:
            return status.HTTP_500_INTERNAL_SERVER_ERROR
        except exceptions.PermissionDenied:
            return status.HTTP_500_INTERNAL_SERVER_ERROR
