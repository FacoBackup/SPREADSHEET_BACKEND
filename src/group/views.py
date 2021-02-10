from rest_framework.decorators import (api_view as route)
from rest_framework.response import Response as callRespond
from src.group.services import GroupFactory, GroupReader
from django.http import HttpResponse
import jwt
import time
from rest_framework import status


@route(['POST'])
def create_group(request):
    return HttpResponse(
        status=GroupFactory.create_group(name=request.data['name'],
                                         about=request.data['about'],
                                         pic=request.data['pic'])
    )


@route(['PATCH'])
def get_group(request):
    return callRespond(
        GroupReader.GroupReadService.read_group(request.data['group_id'])
    )

