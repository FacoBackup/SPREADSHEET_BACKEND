from src.repository.models import Repository, Column, Row
from django.core import exceptions, serializers
from rest_framework import status


class FormReadService:
    @staticmethod
    def read_column_rows(column_id):
        try:
            content = Row.objects.filter(field_fk=column_id)
            response = []
            for i in content:
                response.__iadd__(FormReadService.__map_row(content[i]))

            return response
        except exceptions.ObjectDoesNotExist:
            return status.HTTP_500_INTERNAL_SERVER_ERROR

    @staticmethod
    def read_columns(branch_id):
        try:
            columns = Column.objects.filter(branch_fk=branch_id)
            response = []
            for i in columns:
                response.__iadd__(FormReadService.__map_column(columns[i]))

            return response
        except exceptions.ObjectDoesNotExist:
            return status.HTTP_500_INTERNAL_SERVER_ERROR

    @staticmethod
    def read_all_rows_from_branch(branch_id):
        try:
            response = []
            columns = Column.objects.filter(branch_fk=branch_id)

            for i in columns:
                content = Row.objects.filter(column_fk=columns[i].id)
                mapped_content = []
                for j in content:
                    mapped_content.__iadd__(FormReadService.__map_row(content[j]))

                response.__iadd__(mapped_content)

            return response
        except exceptions.ObjectDoesNotExist:
            return status.HTTP_500_INTERNAL_SERVER_ERROR

    @staticmethod
    def read_all_content_by_branch(branch_id):
        try:
            response = []
            columns = Column.objects.filter(branch_fk=branch_id)

            for i in columns:
                content = Row.objects.filter(column_fk=columns[i].id)
                mapped_content = []
                for j in content:
                    mapped_content.__iadd__(FormReadService.__map_row(content[j]))

                response.__iadd__({
                    "column_id": columns[i].id,
                    "content": mapped_content
                })

            return response
        except exceptions.ObjectDoesNotExist:
            return status.HTTP_500_INTERNAL_SERVER_ERROR

    # @staticmethod
    # def __map_form(form):
    #     return {
    #         "name": form.name,
    #         "about": form.about,
    #         "group_id": form.group_fk,
    #         "id": form.id
    #     }

    @staticmethod
    def __map_column(field):
        return {
            "id": field.id,
            "branch_id": field.branch_fk,
            "name": field.name
        }

    @staticmethod
    def __map_row(content):
        return {
            "content": content.content,
            "id": content.id,
            "column_id": content.column_fk
        }

    # @staticmethod
    # def __map_access(access):
    #     return {
    #         "user_id": access.user_fk,
    #         "br": access.branch_fk
    #     }
