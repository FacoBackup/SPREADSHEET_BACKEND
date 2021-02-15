from rest_framework.decorators import (api_view as route)
from rest_framework.response import Response as callRespond
from src.group.services import GroupFactory, GroupReader
from django.http import HttpResponse


@route(["PATCH"])
def search_group_backward(request):
    return callRespond(
        GroupReader.GroupReadService.search_group(search_input=request.data['search_input'],
                                                  reference_id=request.data['min_id'],
                                                  forward=False)
    )


@route(['POST'])
def create_group(request):
    return HttpResponse(
        status=GroupFactory.create_group(name=request.data['name'],
                                         about=request.data['about'],
                                         pic=request.data['pic'])
    )


@route(['PATCH'])
def get_group_members(request):
    return callRespond(
        GroupReader.GroupReadService.read_group_members(group_id=request.data['group_id'])
    )


@route(['PATCH'])
def search_group(request):
    return callRespond(
        GroupReader.GroupReadService.search_group(search_input=request.data['search_input'],
                                                  reference_id=request.data['max_id'],
                                                  forward=True)
    )


@route(['PATCH'])
def get_group(request):
    return callRespond(
        GroupReader.GroupReadService.read_group(request.data['group_id'])
    )
