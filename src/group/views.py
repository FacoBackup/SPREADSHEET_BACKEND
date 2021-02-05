from rest_framework.decorators import (api_view as route)
from rest_framework.response import Response as callRespond
from src.group.services import GroupFactory, GroupReader
from django.http import HttpResponse
import jwt
import time
from rest_framework import status


@route(['POST'])
def create_group(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    if token is not None:
        decoded_token = jwt.decode(token, key="askdasdiuh123i1y98yejas9d812hiu89dqw9", algorithms="HS256")

        return callRespond(
            GroupFactory.create_group(name=request.data['name'],
                                      about=request.data['about'],
                                      requester=decoded_token['user_id'],
                                      pic=request.data['pic'])
        )
    else:
        return callRespond(status.HTTP_401_UNAUTHORIZED)


@route(['PATCH'])
def get_group(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    if token is not None:
        decoded_token = jwt.decode(token, key="askdasdiuh123i1y98yejas9d812hiu89dqw9", algorithms="HS256")
        if decoded_token['exp'] > time.time():
            return callRespond(
                GroupReader.GroupReadService.read_group(request.data['group_id'])
            )
        else:
            return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)

    else:
        return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)


@route(['PATCH'])
def get_groups_by_user(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    if token is not None:
        decoded_token = jwt.decode(token, key="askdasdiuh123i1y98yejas9d812hiu89dqw9", algorithms="HS256")
        if decoded_token['exp'] > time.time():
            return callRespond(
                GroupReader.GroupReadService.read_groups_user(request.data['user_id'])
            )
        else:
            return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)

    else:
        return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)


@route(['PATCH'])
def get_groups_by_user_max_id(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    if token is not None:
        decoded_token = jwt.decode(token, key="askdasdiuh123i1y98yejas9d812hiu89dqw9", algorithms="HS256")
        if decoded_token['exp'] > time.time():
            return callRespond(
                GroupReader.GroupReadService.read_groups_user_max_id(request.data['user_id'],
                                                                     max_id=request.data['max_id'])
            )
        else:
            return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)

    else:
        return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)
