import jwt
from rest_framework.decorators import (api_view as route)
from rest_framework.response import Response as callRespond
from src.file_management.services.form import FormFactory, FormRead
from src.file_management.services.repository import RepositoryReadService, RepositoryFactory
from rest_framework.views import APIView
from rest_framework import status
from src.user.services import UserRead


@route(['POST'])
def create_repository(request):
    token = request.META.get('HTTP_X_TOKEN')
    if token is not None:
        decoded_token = jwt.decode(token, key="askdasdiuh123i1y98yejas9d812hiu89dqw9", algorithms="HS256")
        return callRespond(
            RepositoryFactory.
            RepositoryFactory.
            create_repository(name=request.data['name'],
                              about=request.data['about'],
                              group_id=request.data['group_id'], requester=decoded_token['user_id'])
        )
    else:
        return callRespond(status.HTTP_401_UNAUTHORIZED)


@route(['POST'])
def create_branch(request):
    token = request.META.get('HTTP_X_TOKEN')
    if token is not None:
        decoded_token = jwt.decode(token, key="askdasdiuh123i1y98yejas9d812hiu89dqw9", algorithms="HS256")

        return callRespond(
            RepositoryFactory.
            RepositoryFactory.
            create_branch(name=request.data['name'],
                          repository_id=request.data['repository_id'],
                          requester=decoded_token['user_id'], about=request.data['about'])
        )
    else:
        return callRespond(status.HTTP_401_UNAUTHORIZED)


@route(['POST'])
def save_changes(request):
    token = request.META.get('HTTP_X_TOKEN')
    if token is not None:
        decoded_token = jwt.decode(token, key="askdasdiuh123i1y98yejas9d812hiu89dqw9", algorithms="HS256")
        return callRespond(
            RepositoryFactory.RepositoryFactory.save_changes(data=request.data, requester=decoded_token['user_id'])
        )
    else:
        return callRespond(status.HTTP_401_UNAUTHORIZED)


@route(['POST'])
def read_group_repositories(request):
    token = request.META.get('HTTP_X_TOKEN')
    if token is not None:
        return callRespond(
            RepositoryReadService.RepositoryReadService.read_group_repositories(group_id=request.data['group_id'])
        )
    else:
        return callRespond(status.HTTP_401_UNAUTHORIZED)


@route(['POST'])
def read_repository_branches(request):
    token = request.META.get('HTTP_X_TOKEN')
    if token is not None:
        return callRespond(
            RepositoryReadService.
            RepositoryReadService.
            read_repository_branches(repository_id=request.data['repository_id'])
        )
    else:
        return callRespond(status.HTTP_401_UNAUTHORIZED)


@route(['POST'])
def read_branch_commits(request):
    token = request.META.get('HTTP_X_TOKEN')
    if token is not None:
        return callRespond(
            RepositoryReadService.RepositoryReadService.read_branch_commits(branch_id=request.data['branch_id'])
        )

    else:
        return callRespond(status.HTTP_401_UNAUTHORIZED)


@route(['POST'])
def create_column(request):
    token = request.META.get('HTTP_X_TOKEN')
    if token is not None:
        return callRespond(
            FormFactory.FormFactory.create_column(name=request.data['name'], branch_id=request.data['branch_id'])
        )

    else:
        return callRespond(status.HTTP_401_UNAUTHORIZED)


@route(['POST'])
def create_cell(request):
    token = request.META.get('HTTP_X_TOKEN')
    if token is not None:
        decoded_token = jwt.decode(token, key="askdasdiuh123i1y98yejas9d812hiu89dqw9", algorithms="HS256")
        return callRespond(
            FormFactory.FormFactory.create_row(content=request.data['content'], requester=decoded_token['user_id'],
                                               column_id=request.data['column_id'])
        )
    else:
        return callRespond(status.HTTP_401_UNAUTHORIZED)


@route(['PATCH'])
def read_all_rows(request):
    token = request.META.get('HTTP_X_TOKEN')
    if token is not None:
        return callRespond(
            FormRead.FormReadService.read_all_content_by_branch(branch_id=request.data['branch_id'])
        )
    else:
        return callRespond(status.HTTP_401_UNAUTHORIZED)


@route(['PATCH'])
def read_all_columns(request):
    token = request.META.get('HTTP_X_TOKEN')
    if token is not None:
        return callRespond(

            FormRead.FormReadService.read_columns(branch_id=request.data['branch_id'])

        )
    else:
        return callRespond(status.HTTP_401_UNAUTHORIZED)


@route(['PATCH'])
def read_all_cells_by_column(request):
    token = request.META.get('HTTP_X_TOKEN')
    if token is not None:
        return callRespond(
            FormRead.FormReadService.read_column_rows(column_id=request.data['column_id'])
        )
    else:
        return callRespond(status.HTTP_401_UNAUTHORIZED)


@route(['PATCH'])
def read_all_content_by_branch(request):
    token = request.META.get('HTTP_X_TOKEN')
    if token is not None:
        return callRespond(
            FormRead.FormReadService.read_all_content_by_branch(branch_id=request.data['branch_id'])
        )
    else:
        return callRespond(status.HTTP_401_UNAUTHORIZED)
