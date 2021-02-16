import jwt
from rest_framework.decorators import (api_view as route)
from rest_framework.response import Response as callRespond
from src.file_management.services.repository import RepositoryFactory
from rest_framework import status
from django.http import HttpResponse
import time


@route(['PUT'])
def add_contributor(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    if token is not None:
        decoded_token = jwt.decode(token, key="askdasdiuh123i1y98yejas9d812hiu89dqw9", algorithms="HS256")
        if decoded_token['exp'] > time.time():
            return callRespond(
                status=RepositoryFactory.RepositoryFactory.add_contributor_branch(user_id=request.data['user_id'],
                                                                                  branch_id=request.data['branch_id'],
                                                                                  requester=decoded_token['user_id'])
            )
        else:
            return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)
    else:
        return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)


@route(['DELETE'])
def remove_contributor(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    if token is not None:
        decoded_token = jwt.decode(token, key="askdasdiuh123i1y98yejas9d812hiu89dqw9", algorithms="HS256")
        if decoded_token['exp'] > time.time():
            return callRespond(
                status=RepositoryFactory.RepositoryFactory.remove_contributor_branch(user_id=request.data['user_id'],
                                                                                     branch_id=request.data[
                                                                                         'branch_id'],
                                                                                     requester=decoded_token['user_id'])
            )
        else:
            return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)
    else:
        return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)
