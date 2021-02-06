import jwt
from rest_framework import status
from rest_framework.decorators import (api_view as route)
from rest_framework.response import Response as callRespond
from django.http import HttpResponse
from src.user.services import UserRead, UserFactory
from src.user.services import Auth
import time


@route(['POST'])
def create_user(request):
    return HttpResponse(status=UserFactory.create_user(nationality=request.data['nationality'],
                                                       name=request.data['name'],
                                                       email=request.data['email'],
                                                       about=request.data['about'],
                                                       phone=request.data['phone'],
                                                       pic=request.data['pic'],
                                                       study=request.data['study'],
                                                       birth=request.data['birth'],
                                                       department=request.data['department']))


@route(['PATCH'])
def get_user_by_id(request):
    data = UserRead.UserReadService.read_user_by_id(request.data['user_id'])
    return callRespond(data)


@route(['PATCH'])
def search_user(request):
    data = UserRead.UserReadService.search_user(search_input=request.data['search_input'])
    return callRespond(data)


@route(['PATCH'])
def get_user_by_max_id(request):
    data = UserRead.UserReadService.read_user_by_max_id(request.data['max_id'])
    return callRespond(data)


@route(['PATCH'])
def get_users(request):
    if request.data['max_id'] is None:
        return callRespond(UserRead.UserReadService.read_users())
    else:
        return callRespond(UserRead.UserReadService.read_user_by_max_id(request.data['max_id']))


@route(['POST'])
def sign_in(request):
    response = Auth.sign_in(user_email=request.data['email'], password=request.data['password'])
    if response == 401:
        return HttpResponse(status=401)
    else:
        return callRespond(response)
