from src.file_management.models import Repository, Column, Cell
from django.core import exceptions, serializers
from rest_framework import status


class FormReadService:
    @staticmethod
    def read_column_cells(column_id):
        try:
            content = Cell.objects.filter(field_fk=column_id)
            response = []
            for i in content:
                response.append(FormReadService.__map_cell(i))

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
    def read_all_cells_from_branch(branch_id):
        try:
            response = []
            columns = Column.objects.filter(branch_fk=branch_id)

            for i in columns:
                content = Cell.objects.filter(column_fk=i.id)
                mapped_content = []
                for j in content:
                    mapped_content.append(FormReadService.__map_cell(j))

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
                content = Cell.objects.filter(column_fk=i.id)
                mapped_content = []
                for j in content:
                    mapped_content.append(
                        str(FormReadService.__map_cell_csv(j.content, column_name=i.name)) +
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

    # [
    #     {
    #         "column_id": 1,
    #         "column_name": "COLUMN 1",
    #         "cells": [
    #             {
    #                 "cell_id": 1,
    #                 "content": "algo"
    #             },
    #             {
    #                 "cell_id": 2,
    #                 "content": "algo dnv"
    #             },
    #             {
    #                 "cell_id": 3,
    #                 "content": "algo dnv dnv"
    #             }
    #         ]
    #     },
    #     {
    #         "column_id": 2,
    #         "column_name": "COLUMN 2",
    #         "cells": [
    #             {
    #                 "cell_id": 4,
    #                 "content": "algo"
    #             },
    #             {
    #                 "cell_id": 5,
    #                 "content": "algo dnv"
    #             },
    #             {
    #                 "cell_id": 6,
    #                 "content": "algo dnv dnv"
    #             }
    #         ]},
    #     {},
    #     {}
    #
    # ]
    @staticmethod
    def read_all_content_by_branch(branch_id):
        try:
            response = []

            columns = Column.objects.filter(branch_fk=branch_id)

            for i in columns:
                content = Cell.objects.filter(column_fk=i.id)
                mapped_content = []
                for j in content:
                    mapped_content.append(FormReadService.__map_cell(j))

                response.append({
                    "column_id": i.id,
                    "column_name": i.name,
                    "cells": mapped_content
                })

            return response
        except exceptions.ObjectDoesNotExist:
            return status.HTTP_500_INTERNAL_SERVER_ERROR

    @staticmethod
    def __map_cell(content):
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
    def __map_cell_csv(content, column_name):
        return column_name + ": " + content

    @staticmethod
    def __map_column(field):
        return {
            "id": field.id,
            "branch_id": field.branch_fk.id,
            "name": field.name
        }

    @staticmethod
    def __map_cell(content):
        return {
            "content": content.content,
            "id": content.id,
            "column_id": content.column_fk.id
        }
