import json
from rest_framework.decorators import (api_view as route)
from rest_framework.response import Response as callRespond
from src.repository.services import FormFactory, FormRead
from rest_framework.views import APIView


class FormViews(APIView):

    @route(['POST'])
    def create_form(self, request):
        return callRespond(
            FormFactory.FormFactory.create_form(name=request.data['name'], about=request.data['about'],
                                                group_id=request.data['group_id'], requester=1)
        )

    @route(['POST'])
    def create_form_field(self, request):
        return callRespond(
            FormFactory.FormFactory.create_column(name=request.data['name'], form_id=request.data['form_id'])
        )

    @route(['POST'])
    def create_field_content(self, request):
        return callRespond(
            FormFactory.FormFactory.create_row(content=request.data['content'], requester=1,
                                               form_field_id=request.data['form_field_id'])
        )

    @route(['PATCH'])
    def read_form_content(self, request):
        return callRespond(
            json.loads(
                FormRead.FormReadService.read_all_content_by_branch(form_id=request.data['form_id'])
            )
        )

    @route(['PATCH'])
    def read_form_fields(self, request):
        return callRespond(
            json.loads(
                FormRead.FormReadService.read_columns(form_id=request.data['form_id'])
            )
        )

    @route(['PATCH'])
    def read_field_content(self, request):
        return callRespond(
            json.loads(
                FormRead.FormReadService.read_column_rows(form_field_id=request.data['form_field_id'])
            )
        )
