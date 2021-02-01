import json
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import (api_view as route)
from rest_framework.response import Response as callRespond
from src.user.services import UserRead, UserFactory
from services import GroupFactory, GroupReader


@route(['POST'])
def create_group(request):
    return callRespond(GroupFactory.create_group(name=request.data['name'], about=request.data['about'], requester=None))


@route(['PATCH'])
def get_group(request):
    return callRespond(GroupReader.read_group(request.data['group_id']))


@route(['PATCH'])
def get_groups_by_user(request):
    return callRespond(GroupReader.read_groups_user(request.data['user_id']))


@route(['PATCH'])
def get_groups_by_user_max_id(request):
    return callRespond(GroupReader.read_groups_user_max_id(request.data['user_id'], max_id=request.data['max_id']))

