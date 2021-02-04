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
                response.append(FormReadService.__map_row(i))

            return response
        except exceptions.ObjectDoesNotExist:
            return status.HTTP_500_INTERNAL_SERVER_ERROR

    @staticmethod
    def read_columns(branch_id):
        try:
            columns = Column.objects.filter(branch_fk=branch_id)
            response = []
            for i in columns:
                response.append(FormReadService.__map_column(i))

            return response
        except exceptions.ObjectDoesNotExist:
            return status.HTTP_500_INTERNAL_SERVER_ERROR

    @staticmethod
    def read_all_rows_from_branch(branch_id):
        try:
            response = []
            columns = Column.objects.filter(branch_fk=branch_id)

            for i in columns:
                content = Row.objects.filter(column_fk=i.id)
                mapped_content = []
                for j in content:
                    mapped_content.append(FormReadService.__map_row(j))

                response.append(mapped_content)

            return response
        except exceptions.ObjectDoesNotExist:
            return status.HTTP_500_INTERNAL_SERVER_ERROR

    @staticmethod
    def export_json_to_csv(branch_id):
        try:
            response = []
            columns = Column.objects.filter(branch_fk=branch_id)

            for i in columns:
                content = Row.objects.filter(column_fk=i.id)
                mapped_content = []
                for j in content:
                    mapped_content.append(
                        str(FormReadService.__map_row_csv(j.content, column_name=i.name)) +
                        FormReadService.__add_comma(position=content.index(j), size=len(content) - 1)
                    )
                e = 0
                response.append(
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
                content = Row.objects.filter(column_fk=i.id)
                mapped_content = []
                for j in content:
                    mapped_content.append(FormReadService.__map_row(j))

                response.append({
                    "column": {
                        "name": i.name,
                        "id": i.id
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
            "branch_id": field.branch_fk.id,
            "name": field.name
        }

    @staticmethod
    def __map_row(content):
        return {
            "content": content.content,
            "id": content.id,
            "column_id": content.column_fk.id
        }
