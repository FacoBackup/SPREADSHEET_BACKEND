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
def export_formatted_json(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    if token is not None:
        decoded_token = jwt.decode(token, key="askdasdiuh123i1y98yejas9d812hiu89dqw9", algorithms="HS256")
        if decoded_token['exp'] > datetime.datetime.now().timestamp() * 1000:
            return callRespond(FormReader.FormReadService.formatted_json(branch_id=int(request.GET.get('branch_id'))))
        else:
            return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)
    else:
        return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)


@route(['GET'])
def check_access(request):
    token = request.META.get('HTTP_AUTHORIZATION')

    if token is not None:
        decoded_token = jwt.decode(token, key="askdasdiuh123i1y98yejas9d812hiu89dqw9", algorithms="HS256")
        print("token :" + str(decoded_token['exp']))
        if decoded_token['exp'] > datetime.datetime.now().timestamp() * 1000:
            return callRespond(RepositoryReader.RepositoryReadService.check_access(user_id=decoded_token['user_id'],
                                                                                   branch_id=int(
                                                                                       request.GET.get("branch_id")
                                                                                   )))

        else:
            return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)
    else:
        return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)


@route(['GET'])
def read_branch_contributors(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    if token is not None:
        decoded_token = jwt.decode(token, key="askdasdiuh123i1y98yejas9d812hiu89dqw9", algorithms="HS256")
        if decoded_token['exp'] > datetime.datetime.now().timestamp() * 1000:
            return callRespond(
                RepositoryReader.RepositoryReadService.read_branch_contributors(
                    branch_id=int(request.GET.get('branch_id')))
            )
        else:
            return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)
    else:
        return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)


@route(['GET'])
def read_all_content_by_branch(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    if token is not None:
        decoded_token = jwt.decode(token, key="askdasdiuh123i1y98yejas9d812hiu89dqw9", algorithms="HS256")
        if decoded_token['exp'] > datetime.datetime.now().timestamp() * 1000:
            return callRespond(
                FormReader.FormReadService.read_all_content_by_branch(branch_id=int(request.GET.get('branch_id')))
            )
        else:
            return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)
    else:
        return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)


@route(['PATCH'])
def read_repository_branches(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    if token is not None:
        decoded_token = jwt.decode(token, key="askdasdiuh123i1y98yejas9d812hiu89dqw9", algorithms="HS256")
        if decoded_token['exp'] > datetime.datetime.now().timestamp() * 1000:
            return callRespond(
                RepositoryReader.
                    RepositoryReadService.
                    read_repository_branches(repository_id=request.data['repository_id'])
            )
        else:
            return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)
    else:
        return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)


@route(['GET'])
def verify_branch_name(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    if token is not None:
        decoded_token = jwt.decode(token, key="askdasdiuh123i1y98yejas9d812hiu89dqw9", algorithms="HS256")
        if decoded_token['exp'] > datetime.datetime.now().timestamp() * 1000:
            return callRespond(
                status=RepositoryReader.RepositoryReadService.verify_branch_by_name(name=request.GET.get('name'))
            )
        else:
            return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)
    else:
        return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)


@route(['POST'])
def create_branch(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    if token is not None:
        decoded_token = jwt.decode(token, key="askdasdiuh123i1y98yejas9d812hiu89dqw9", algorithms="HS256")
        if decoded_token['exp'] > datetime.datetime.now().timestamp() * 1000:
            response = (RepositoryFactory.
                        RepositoryFactory.
                        create_branch(name=request.data['name'],
                                      target_branch_id=request.data['target_branch_id'],
                                      requester=decoded_token['user_id']))
            if response is None:
                return callRespond(
                    status=409
                )
            else:
                return callRespond(response)
        else:
            return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)
    else:
        return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)


@route(['GET'])
def read_contributor_branches(request):
    if request.GET.get('max_id') is None:
        return callRespond(RepositoryReader.RepositoryReadService.read_branches_user(
            user_id=int(request.GET.get('user_id')))
        )
    else:
        return callRespond(RepositoryReader.RepositoryReadService.read_branches_user_by_max_id(
            max_id=int(request.GET.get('max_id')),
            user_id=int(request.GET.get('user_id'))
        ))


@route(['PUT'])
def merge_branches(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    if token is not None:
        decoded_token = jwt.decode(token, key="askdasdiuh123i1y98yejas9d812hiu89dqw9", algorithms="HS256")
        if decoded_token['exp'] > datetime.datetime.now().timestamp() * 1000:
            return callRespond(
                status=RepositoryFactory.RepositoryFactory.merge(source_branch_id=request.data['source_branch_id'],
                                                                 requester=decoded_token['user_id'])
            )
        else:
            return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)
    else:
        return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)


@route(['PATCH'])
def verify_member_by_branch(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    if token is not None:
        decoded_token = jwt.decode(token, key="askdasdiuh123i1y98yejas9d812hiu89dqw9", algorithms="HS256")
        if decoded_token['exp'] > datetime.datetime.now().timestamp() * 1000:
            return callRespond(
                RepositoryReader.RepositoryReadService.verify_member_by_branch(user_id=decoded_token['user_id'],
                                                                               branch_id=request.data['branch_id'])
            )
        else:
            return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)
    else:
        return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)


@route(['GET'])
def read_branch(request):
    data = RepositoryReader.RepositoryReadService.read_branch(branch_id=int(request.GET.get('branch_id')))

    if data is not None:
        return callRespond(data)
    else:
        return HttpResponse(status=404)


@route(["PATCH"])
def search_branch_backwards(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    if token is not None:
        decoded_token = jwt.decode(token, key="askdasdiuh123i1y98yejas9d812hiu89dqw9", algorithms="HS256")
        if decoded_token['exp'] > datetime.datetime.now().timestamp() * 1000:
            return callRespond(RepositoryReader.RepositoryReadService.search_branch(
                search_input=request.data['search_input'],
                reference_id=request.data['min_id'],
                forward=False))

        else:
            return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)
    else:
        return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)


@route(["PATCH"])
def search_branch(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    if token is not None:
        decoded_token = jwt.decode(token, key="askdasdiuh123i1y98yejas9d812hiu89dqw9", algorithms="HS256")
        if decoded_token['exp'] > datetime.datetime.now().timestamp() * 1000:
            return callRespond(RepositoryReader.RepositoryReadService.search_branch(
                search_input=request.data['search_input'],
                reference_id=request.data['max_id'],
                forward=True)
            )

        else:
            return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)
    else:
        return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)
