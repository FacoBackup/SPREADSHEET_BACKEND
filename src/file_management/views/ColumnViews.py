import jwt
from rest_framework.decorators import (api_view as route)
from rest_framework.response import Response as callRespond
from src.file_management.services.form import FormFactory, FormReader
from src.file_management.services.repository import RepositoryReader, RepositoryFactory
from rest_framework import status
from django.http import HttpResponse
import time


@route(['PUT'])
def update_column(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    if token is not None:
        decoded_token = jwt.decode(token, key="askdasdiuh123i1y98yejas9d812hiu89dqw9", algorithms="HS256")
        if decoded_token['exp'] > time.time():
            data = RepositoryFactory.RepositoryFactory.update_column(column_id=request.data['column_id'],
                                                                     name=request.data['name'],
                                                                     user_id=decoded_token['user_id'])
            if data is not None:
                return HttpResponse(data)
            else:
                return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        else:
            return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)
    else:
        return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)


@route(['POST'])
def create_column(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    if token is not None:
        decoded_token = jwt.decode(token, key="askdasdiuh123i1y98yejas9d812hiu89dqw9", algorithms="HS256")
        if decoded_token['exp'] > time.time():
            return HttpResponse(status=FormFactory.FormFactory.create_column(name=request.data['name'],
                                                                             branch_id=request.data['branch_id']))
        else:
            return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)
    else:
        return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)
