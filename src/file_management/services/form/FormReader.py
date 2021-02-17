from django.db.models import Max

from src.file_management.models import Repository, Column, Cell
from django.core import exceptions, serializers
from rest_framework import status
import json


class FormReadService:
    @staticmethod
    def read_column_cells(column_id):
        try:
            content = Cell.objects.filter(field_fk=column_id)
            response = []
            for i in content:
                response.append(FormReadService.map_cell(i))

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
                    mapped_content.append(FormReadService.map_cell(j))

                response.append(mapped_content)

            return response
        except exceptions.ObjectDoesNotExist:
            return status.HTTP_500_INTERNAL_SERVER_ERROR

    @staticmethod
    def __map_cell_json(cell):
        return {cell.column_fk.name: cell.content}

    @staticmethod
    def formatted_json(branch_id):
        try:
            max_row = Cell.objects.aggregate(Max('row'))['row__max']
            objects = []
            response = []

            for i in range(max_row + 1):
                row = []
                row_cells = Cell.objects.filter(column_fk__branch_fk__id=branch_id, row=i).order_by('column_fk__id')

                for j in row_cells:
                    row.append(FormReadService.__map_cell_json(j))

                objects.append(row)
            for j in range(len(objects)):
                response.append(json.loads(
                    json.dumps(objects[j]).replace('{', "").replace('}', "").replace('[', "{").replace(']', "}")))
            return response
        except exceptions.ObjectDoesNotExist:
            return status.HTTP_500_INTERNAL_SERVER_ERROR

    @staticmethod
    def read_all_content_by_branch(branch_id):
        try:
            response = []

            columns = Column.objects.filter(branch_fk=branch_id).order_by('id')

            for i in columns:
                content = Cell.objects.filter(column_fk=i.id).order_by('id')
                mapped_content = []
                for j in content:
                    mapped_content.append(FormReadService.map_cell(j))

                response.append({
                    "column_id": i.id,
                    "column_name": i.name,
                    "cells": mapped_content
                })

            return response
        except exceptions.ObjectDoesNotExist:
            return status.HTTP_500_INTERNAL_SERVER_ERROR

    @staticmethod
    def __map_column(field):
        return {
            "id": field.id,
            "branch_id": field.branch_fk.id,
            "name": field.name
        }

    @staticmethod
    def map_cell(content):
        return {
            "content": content.content,
            "id": content.id,
            "column_id": content.column_fk.id,
            "row": content.row
        }
