import json
from rest_framework import status
from rest_framework.decorators import (api_view as route)
from rest_framework.response import Response as callRespond
from src.form.services import FormRead, FormFactory


@route(['POST'])
def create_form(request):
    return callRespond(
        FormFactory.FormFactory.create_form(name=request.data['name'], about=request.data['about'],
                                            group_id=request.data['group_id'], requester=1)
    )


@route(['POST'])
def create_form_field(request):
    return callRespond(
        FormFactory.FormFactory.create_form_field(name=request.data['name'], form_id=request.data['form_id'])
    )


@route(['POST'])
def create_field_content(request):
    return callRespond(
        FormFactory.FormFactory.create_form_field_content(content=request.data['content'], requester=1,
                                                          form_field_id=request.data['form_field_id'])
    )


@route(['PATCH'])
def read_form_content(request):
    return callRespond(
        json.loads(
            FormRead.FormReadService.read_all_content_form(form_id=request.data['form_id'])
        )
    )


@route(['PATCH'])
def read_form_fields(request):
    return callRespond(
        json.loads(
            FormRead.FormReadService.read_form_fields(form_id=request.data['form_id'])
        )
    )


@route(['PATCH'])
def read_field_content(request):
    return callRespond(
        json.loads(
            FormRead.FormReadService.read_form_field_content(form_field_id=request.data['form_field_id'])
        )
    )
