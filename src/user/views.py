import json
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import (api_view as route)
from rest_framework.response import Response as callRespond
from src.user.services import UserRead, UserFactory
from src.user.services import Auth


@route(['GET'])
def test():
    return callRespond("WORKS")


@route(['POST'])
def create_user(request):
    return callRespond(UserFactory.create_user(nationality=request.data['nationality'],
                                               name=request.data['name'],
                                               email=request.data['email'],
                                               about=request.data['about'],
                                               phone=request.data['phone'],
                                               pic=request.data['pic'],
                                               study=request.data['study'],
                                               birth=request.data['birth']))


@route(['PATCH'])
def get_user_by_id(request):
    data = UserRead.read_user_by_id(request.data['id'])
    print(data)
    return callRespond(json.loads(data))


@route(['PATCH'])
def get_user_by_max_id(request):
    data = UserRead.read_user_by_max_id(request.data['max_id'])
    # JsonResponse(UserRead.read_user_by_max_id(request.data['max_id']), safe=False)
    return callRespond(json.loads(data))


@route(['GET'])
def get_users(request):
    return callRespond(UserRead.read_users())


@route(['POST'])
def sign_in(request):
    return callRespond(Auth.sign_in(request.data['email']))