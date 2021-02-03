from src.file_management.models import Repository, Column, Row
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
    def export_json_to_csv(branch_id):
        try:
            response = []
            columns = Column.objects.filter(branch_fk=branch_id)

            for i in columns:
                content = Row.objects.filter(column_fk=columns[i].id)
                mapped_content = []
                for j in content:
                    mapped_content.__iadd__(
                        str(FormReadService.__map_row_csv(content[j].content, column_name=columns[i].name)) +
                        FormReadService.__add_comma(position=j, size=len(content) - 1)
                    )
                e = 0
                response.__iadd__(
                    "{" +
                    ", ".join(mapped_content)
                    +
                    " }"
                )

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
                    "column": {
                        "name": columns[i].name,
                        "id": columns[i].id
                    },
                    "content": mapped_content
                })

            return response
        except exceptions.ObjectDoesNotExist:
            return status.HTTP_500_INTERNAL_SERVER_ERROR

    @staticmethod
    def __map_row(content):
        return {
            "content": content.content,
            "id": content.id
        }

    @staticmethod
    def __add_comma(position, size):
        if position < size:
            return ", "
        else:
            return ""

    @staticmethod
    def __map_row_csv(content, column_name):
        return column_name + ": " + content

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
