import jwt
from rest_framework import status
from rest_framework.decorators import (api_view as route)
from rest_framework.response import Response as callRespond
from src.user.services import UserRead, UserFactory
from src.user.services import Auth
from rest_framework.views import APIView


@route(['POST'])
def create_user(request):
    return callRespond(UserFactory.create_user(nationality=request.data['nationality'],
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
    token = request.META.get('HTTP_X_TOKEN')
    if token is not None:
        decoded_token = jwt.decode(str(token), key="askdasdiuh123i1y98yejas9d812hiu89dqw9", algorithms="HS256")
        print(decoded_token)
        data = UserRead.UserReadService.read_user_by_id(decoded_token["user_id"])
        if data is not None:
            return callRespond(data)
        else:
            return callRespond(status.HTTP_404_NOT_FOUND)
    else:
        return callRespond(status.HTTP_401_UNAUTHORIZED)


@route(['PATCH'])
def get_user_by_max_id(request):
    token = request.META.get('HTTP_X_TOKEN')
    if token is not None:
        data = UserRead.UserReadService.read_user_by_max_id(request.data['max_id'])
        if data is not None:
            return callRespond(data)
        else:
            return callRespond(status.HTTP_404_NOT_FOUND)
    else:
        return callRespond(status.HTTP_401_UNAUTHORIZED)


@route(['GET'])
def get_users(request):
    return callRespond(UserRead.UserReadService.read_users())


@route(['POST'])
def sign_in(request):
    return callRespond(Auth.sign_in(user_email=request.data['email'], password=request.data['password']))
