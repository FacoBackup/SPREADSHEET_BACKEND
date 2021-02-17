import datetime

import jwt
from rest_framework.decorators import (api_view as route)
from rest_framework.response import Response as callRespond
from src.file_management.services.form import FormFactory, FormReader
from src.file_management.services.repository import RepositoryReader, RepositoryFactory
from rest_framework import status
from django.http import HttpResponse
import time


@route(['GET'])
def verify_open_commit(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    if token is not None:
        decoded_token = jwt.decode(token, key="askdasdiuh123i1y98yejas9d812hiu89dqw9", algorithms="HS256")
        if decoded_token['exp'] > datetime.datetime.now().timestamp() * 1000:
            return callRespond(
                RepositoryReader.RepositoryReadService.verify_open_commit(branch_id=int(request.GET.get('branch_id'))))
        else:
            return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)
    else:
        return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)


@route(['GET'])
def read_latest_commits(request):
    response = RepositoryReader.RepositoryReadService.read_latest_commits(user_id=int(request.GET.get('user_id')))
    return callRespond(
        response
    )


@route(['POST'])
def make_commit(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    if token is not None:
        decoded_token = jwt.decode(token, key="askdasdiuh123i1y98yejas9d812hiu89dqw9", algorithms="HS256")
        if decoded_token['exp'] > datetime.datetime.now().timestamp() * 1000:
            return HttpResponse(
                status=RepositoryFactory.RepositoryFactory.commit(
                    branch_id=request.data['branch_id'],
                    user_id=decoded_token['user_id'],
                )
            )
        else:
            return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)
    else:
        return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)


@route(['GET'])
def read_branch_commits(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    if token is not None:
        decoded_token = jwt.decode(token, key="askdasdiuh123i1y98yejas9d812hiu89dqw9", algorithms="HS256")
        if decoded_token['exp'] > datetime.datetime.now().timestamp() * 1000:
            return callRespond(
                RepositoryReader.RepositoryReadService.read_branch_commits(branch_id=int(request.GET.get('branch_id')))
            )
        else:
            return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)
    else:
        return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)
