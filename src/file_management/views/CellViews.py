import jwt
from rest_framework.decorators import (api_view as route)
from rest_framework.response import Response as callRespond
from src.file_management.services.form import FormFactory, FormReader
from src.file_management.services.repository import RepositoryReader, RepositoryFactory
from rest_framework import status
from django.http import HttpResponse
import time


@route(['DELETE'])
def delete_cell(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    if token is not None:
        decoded_token = jwt.decode(token, key="askdasdiuh123i1y98yejas9d812hiu89dqw9", algorithms="HS256")
        if decoded_token['exp'] > time.time():
            data = RepositoryFactory.RepositoryFactory.delete_cell(cell_id=request.data['cell_id'],
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
def create_cell(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    if token is not None:
        decoded_token = jwt.decode(token, key="askdasdiuh123i1y98yejas9d812hiu89dqw9", algorithms="HS256")
        if decoded_token['exp'] > time.time():
            response = FormFactory.FormFactory.create_cell(content=request.data['content'],
                                                           row=request.data['row'],
                                                           column_id=request.data['column_id'],
                                                           user_id=decoded_token['user_id'])

            if response is None:
                return callRespond(
                    status=500
                )
            else:
                return callRespond(response)
        else:
            return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)
    else:
        return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)


@route(['GET'])
def read_all_cells(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    if token is not None:
        decoded_token = jwt.decode(token, key="askdasdiuh123i1y98yejas9d812hiu89dqw9", algorithms="HS256")
        if decoded_token['exp'] > time.time():
            return callRespond(
                FormReader.FormReadService.read_all_content_by_branch(
                    branch_id=int(request.GET.get('branch_id'))
                )
            )
        else:
            return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)
    else:
        return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)


@route(['PUT'])
def update_cell(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    if token is not None:
        decoded_token = jwt.decode(token, key="askdasdiuh123i1y98yejas9d812hiu89dqw9", algorithms="HS256")
        if decoded_token['exp'] > time.time():
            return callRespond(
                status=RepositoryFactory.RepositoryFactory.update_cell(content=request.data['content'],
                                                                       cell_id=request.data['cell_id'],
                                                                       user_id=decoded_token['user_id'])
            )
        else:
            return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)
    else:
        return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)
