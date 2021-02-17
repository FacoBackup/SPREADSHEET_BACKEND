from rest_framework.decorators import (api_view as route)
from rest_framework.response import Response as callRespond
from src.group.services import GroupFactory, GroupReader
from django.http import HttpResponse


@route(["GET"])
def search_group_backward(request):
    return callRespond(
        GroupReader.GroupReadService.search_group(search_input=request.GET.get('search_input'),
                                                  reference_id=int(request.GET.get('min_id')),
                                                  forward=False)
    )


@route(['GET'])
def search_group(request):
    return callRespond(
        GroupReader.GroupReadService.search_group(search_input=request.GET.get('search_input'),
                                                  reference_id=int(request.GET.get('max_id')),
                                                  forward=True)
    )


@route(['POST'])
def create_group(request):
    return HttpResponse(
        status=GroupFactory.create_group(name=request.data['name'],
                                         about=request.data['about'],
                                         pic=request.data['pic'])
    )


@route(['GET'])
def get_group_members(request):
    return callRespond(
        GroupReader.GroupReadService.read_group_members(group_id=int(request.GET.get('group_id')))
    )


@route(['GET'])
def get_group(request):
    return callRespond(
        GroupReader.GroupReadService.read_group(int(request.GET.get('group_id')))
    )
