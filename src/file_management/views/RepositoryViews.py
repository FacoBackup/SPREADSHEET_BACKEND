import jwt
from rest_framework.decorators import (api_view as route)
from rest_framework.response import Response as callRespond
from src.file_management.services.form import FormFactory, FormReader
from src.file_management.services.repository import RepositoryReader, RepositoryFactory
from rest_framework import status
from django.http import HttpResponse
import time


@route(['POST'])
def create_repository(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    if token is not None:
        decoded_token = jwt.decode(token, key="askdasdiuh123i1y98yejas9d812hiu89dqw9", algorithms="HS256")
        if decoded_token['exp'] > time.time():
            return callRespond(
                status=RepositoryFactory.RepositoryFactory.create_repository(
                    name=request.data['name'],
                    about=request.data['about'],
                    group_id=request.data['group_id'],
                    requester=decoded_token['user_id']
                )
            )
        else:
            return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)
    else:
        return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)


@route(['GET'])
def get_repository(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    if token is not None:
        decoded_token = jwt.decode(token, key="askdasdiuh123i1y98yejas9d812hiu89dqw9", algorithms="HS256")
        if decoded_token['exp'] > time.time():
            data = RepositoryReader.RepositoryReadService.read_repository(
                repository_id=int(request.GET.get('repository_id'))
            )
            if data is not None:
                return callRespond(data)
            else:
                return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        else:
            return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)
    else:
        return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)


@route(['GET'])
def read_group_repositories(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    if token is not None:
        decoded_token = jwt.decode(token, key="askdasdiuh123i1y98yejas9d812hiu89dqw9", algorithms="HS256")
        if decoded_token['exp'] > time.time():
            return callRespond(
                RepositoryReader.RepositoryReadService.read_group_repositories(
                    group_id=int(request.GET.get('group_id'))
                )
            )
        else:
            return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)
    else:
        return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)
