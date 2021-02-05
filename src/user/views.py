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
    token = request.META.get('HTTP_AUTHORIZATION')
    if token is not None:
        decoded_token = jwt.decode(token, key="askdasdiuh123i1y98yejas9d812hiu89dqw9", algorithms="HS256")
        if decoded_token['exp'] > time.time():
            data = UserRead.UserReadService.read_user_by_id(request.data['user_id'])
            if data is not None:
                return callRespond(data)
            else:
                return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        else:
            return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)

    else:
        print("token not valid")
        return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)


@route(['PATCH'])
def get_user_by_max_id(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    if token is not None:
        decoded_token = jwt.decode(token, key="askdasdiuh123i1y98yejas9d812hiu89dqw9", algorithms="HS256")
        if decoded_token['exp'] > time.time():
            data = UserRead.UserReadService.read_user_by_max_id(request.data['max_id'])
            return callRespond(data)

        else:
            print("TOKEN EXPIRED")
            return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)

    else:
        print("NO TOKEN")
        return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)


@route(['GET'])
def get_users(request):
    return callRespond(UserRead.UserReadService.read_users())


@route(['POST'])
def sign_in(request):
    response = Auth.sign_in(user_email=request.data['email'], password=request.data['password'])
    if response == 401:
        return HttpResponse(status=401)
    else:
        return callRespond(response)
