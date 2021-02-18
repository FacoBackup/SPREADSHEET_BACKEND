import time
import datetime
import jwt
from rest_framework import status
from rest_framework.decorators import (api_view as route)
from rest_framework.response import Response as callRespond
from django.http import HttpResponse
from src.user.services import UserReader, UserFactory
from src.user.services import Auth


@route(["GET"])
def get_user_by_email(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    if token is not None:
        decoded_token = jwt.decode(token, key="askdasdiuh123i1y98yejas9d812hiu89dqw9", algorithms="HS256")
        if decoded_token['exp'] > datetime.datetime.now().timestamp() * 1000:
            user = UserReader.UserReadService.read_user_by_id(user_id=decoded_token['user_id'])
            if user is not None and user['email'] != request.GET.get('email'):
                data = UserReader.UserReadService.read_user_by_email(email=request.GET.get('email'))
                if data is not None:
                    return callRespond(data)
                else:
                    return callRespond(status=404)
            else:
                return callRespond(status=409)
        else:
            return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)
    else:
        return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)


@route(["GET"])
def search_user_backward(request):
    data = UserReader.UserReadService.search_user(search_input=request.GET.get('search_input'),
                                                  reference_id=int(request.GET.get('min_id')),
                                                  forward=True)
    return callRespond(data)


@route(['GET'])
def search_user(request):
    data = UserReader.UserReadService.search_user(search_input=request.GET.get('search_input'),
                                                  reference_id=int(request.GET.get('max_id')),
                                                  forward=True)
    return callRespond(data)


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


@route(['PUT'])
def update_profile(request):
    response = UserFactory.update_profile(user_id=request.data['user_id'],
                                          phone=request.data['phone'],
                                          pic=request.data['pic'],
                                          background=request.data['background'],
                                          about=request.data['about'],
                                          study=request.data['study'])
    return HttpResponse(status=response)


@route(['GET'])
def get_user_by_id(request):
    data = UserReader.UserReadService.read_user_by_id(int(request.GET.get('user_id')))
    if data is not None:
        return callRespond(data)
    else:
        return callRespond(status=404)


@route(['GET'])
def get_users(request):
    if request.GET.get('max_id') is None:
        return callRespond(UserReader.UserReadService.read_users())
    else:
        return callRespond(UserReader.UserReadService.read_user_by_max_id(int(request.GET.get('max_id'))))


@route(['POST'])
def sign_in(request):
    response = Auth.sign_in(user_email=request.data['email'], password=request.data['password'])
    if response == 401:
        return HttpResponse(status=response)
    else:
        return callRespond(response)
