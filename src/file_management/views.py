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
            data = RepositoryFactory.RepositoryFactory.delete_cell(cell_id=request.data['cell_id'])
            if data is not None:
                return HttpResponse(data)
            else:
                return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        else:
            return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)
    else:
        return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)


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


@route(['PATCH'])
def get_repository(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    if token is not None:
        decoded_token = jwt.decode(token, key="askdasdiuh123i1y98yejas9d812hiu89dqw9", algorithms="HS256")
        if decoded_token['exp'] > time.time():
            data = RepositoryReader.RepositoryReadService.read_repository(repository_id=request.data['repository_id'])
            if data is not None:
                return callRespond(data)
            else:
                return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        else:
            return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)
    else:
        return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)


@route(['POST'])
def make_commit(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    if token is not None:
        decoded_token = jwt.decode(token, key="askdasdiuh123i1y98yejas9d812hiu89dqw9", algorithms="HS256")
        if decoded_token['exp'] > time.time():
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


@route(['PATCH'])
def read_contributor_branches(request):
    if request.data['max_id'] is None:
        return callRespond(RepositoryReader.RepositoryReadService.read_branches_user(user_id=request.data['user_id']))
    else:
        return callRespond(RepositoryReader.RepositoryReadService.
                           read_branches_user_by_max_id(max_id=request.data['max_id'], user_id=request.data['user_id']))


@route(['PATCH'])
def read_latest_commits(request):
    response = RepositoryReader.RepositoryReadService.read_latest_commits(user_id=request.data['user_id'])
    return callRespond(
        response
    )


@route(['PATCH'])
def read_branch(request):
    data = RepositoryReader.RepositoryReadService.read_branch(branch_id=request.data['branch_id'])

    if data is not None:
        return callRespond(data)
    else:
        return HttpResponse(status=404)


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


@route(['PATCH'])
def verify_member_by_branch(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    if token is not None:
        decoded_token = jwt.decode(token, key="askdasdiuh123i1y98yejas9d812hiu89dqw9", algorithms="HS256")
        if decoded_token['exp'] > time.time():
            return callRespond(
                RepositoryReader.RepositoryReadService.verify_member_by_branch(user_id=decoded_token['user_id'],
                                                                               branch_id=request.data['branch_id'])
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


@route(['PUT'])
def merge_branches(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    if token is not None:
        decoded_token = jwt.decode(token, key="askdasdiuh123i1y98yejas9d812hiu89dqw9", algorithms="HS256")
        if decoded_token['exp'] > time.time():
            return callRespond(
                status=RepositoryFactory.RepositoryFactory.merge(source_branch_id=request.data['source_branch_id'],
                                                                 requester=decoded_token['user_id'])
            )
        else:
            return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)
    else:
        return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)


@route(['POST'])
def create_repository(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    if token is not None:
        decoded_token = jwt.decode(token, key="askdasdiuh123i1y98yejas9d812hiu89dqw9", algorithms="HS256")
        if decoded_token['exp'] > time.time():
            return callRespond(
                status=RepositoryFactory.
                    RepositoryFactory.
                    create_repository(name=request.data['name'],
                                      about=request.data['about'],
                                      group_id=request.data['group_id'],
                                      requester=decoded_token['user_id'])
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
        if decoded_token['exp'] > time.time():
            return callRespond(
                status=RepositoryFactory.
                    RepositoryFactory.
                    create_branch(name=request.data['name'],
                                  target_branch_id=request.data['target_branch_id'],
                                  requester=decoded_token['user_id'], about=request.data['about'])
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


@route(['PATCH'])
def export_formatted_json(request):
    return callRespond(FormReader.FormReadService.formatted_json(branch_id=request.data['branch_id']))


@route(['PATCH'])
def read_group_repositories(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    if token is not None:
        decoded_token = jwt.decode(token, key="askdasdiuh123i1y98yejas9d812hiu89dqw9", algorithms="HS256")
        if decoded_token['exp'] > time.time():
            return callRespond(
                RepositoryReader.RepositoryReadService.read_group_repositories(group_id=request.data['group_id'])
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
        if decoded_token['exp'] > time.time():
            return callRespond(
                RepositoryReader.
                RepositoryReadService.
                read_repository_branches(repository_id=request.data['repository_id'])
            )
        else:
            return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)
    else:
        return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)


@route(['PATCH'])
def read_branch_commits(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    if token is not None:
        decoded_token = jwt.decode(token, key="askdasdiuh123i1y98yejas9d812hiu89dqw9", algorithms="HS256")
        if decoded_token['exp'] > time.time():
            return callRespond(
                RepositoryReader.RepositoryReadService.read_branch_commits(branch_id=request.data['branch_id'])
            )
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


@route(['PATCH'])
def read_branch_contributors(request):
    return callRespond(
        RepositoryReader.RepositoryReadService.read_branch_contributors(branch_id=request.data['branch_id'])
    )


@route(['POST'])
def create_cell(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    if token is not None:
        decoded_token = jwt.decode(token, key="askdasdiuh123i1y98yejas9d812hiu89dqw9", algorithms="HS256")
        if decoded_token['exp'] > time.time():

            return callRespond(
                status=FormFactory.FormFactory.create_cell(content=request.data['content'],
                                                           row=request.data['row'],
                                                           column_id=request.data['column_id'],
                                                           user_id=decoded_token['user_id'])
            )
        else:
            return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)
    else:
        return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)


@route(['PATCH'])
def read_all_cells(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    if token is not None:
        decoded_token = jwt.decode(token, key="askdasdiuh123i1y98yejas9d812hiu89dqw9", algorithms="HS256")
        if decoded_token['exp'] > time.time():
            return callRespond(
                FormReader.FormReadService.read_all_content_by_branch(branch_id=request.data['branch_id'])
            )
        else:
            return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)
    else:
        return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)


@route(['PATCH'])
def read_all_content_by_branch(request):
    return callRespond(
        FormReader.FormReadService.read_all_content_by_branch(branch_id=request.data['branch_id'])
    )
