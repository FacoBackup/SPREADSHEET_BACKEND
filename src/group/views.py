from rest_framework.decorators import (api_view as route)
from rest_framework.response import Response as callRespond
from src.group.services import GroupFactory, GroupReader
from rest_framework.views import APIView
import jwt
from src.user.services import UserRead
from rest_framework import status


class GroupViews(APIView):

    @route(['POST'])
    def create_group(self, request):
        token = request.META['HTTP_X_TOKEN']
        decoded_token = jwt.decode(token, key="askdasdiuh123i1y98yejas9d812hiu89dqw9", algorithms="HS256")

        if UserRead.UserReadService.read_user_by_id(user_id=decoded_token['user_id']) is not None:
            return callRespond(
                GroupFactory.create_group(name=request.data['name'],
                                          about=request.data['about'],
                                          requester=decoded_token['user_id'],
                                          pic=request.data['pic'])
            )
        else:
            return callRespond(status.HTTP_401_UNAUTHORIZED)

    @route(['PATCH'])
    def get_group(self, request):
        token = request.META['HTTP_X_TOKEN']
        decoded_token = jwt.decode(token, key="askdasdiuh123i1y98yejas9d812hiu89dqw9", algorithms="HS256")

        if UserRead.UserReadService.read_user_by_id(user_id=decoded_token['user_id']) is not None:
            return callRespond(
                GroupReader.GroupReadService.read_group(request.data['group_id'])
            )
        else:
            return callRespond(status.HTTP_401_UNAUTHORIZED)

    @route(['PATCH'])
    def get_groups_by_user(self, request):
        token = request.META['HTTP_X_TOKEN']
        decoded_token = jwt.decode(token, key="askdasdiuh123i1y98yejas9d812hiu89dqw9", algorithms="HS256")

        if UserRead.UserReadService.read_user_by_id(user_id=decoded_token['user_id']) is not None:
            return callRespond(
                GroupReader.GroupReadService.read_groups_user(request.data['user_id'])
            )
        else:
            return callRespond(status.HTTP_401_UNAUTHORIZED)

    @route(['PATCH'])
    def get_groups_by_user_max_id(self, request):
        token = request.META['HTTP_X_TOKEN']
        decoded_token = jwt.decode(token, key="askdasdiuh123i1y98yejas9d812hiu89dqw9", algorithms="HS256")

        if UserRead.UserReadService.read_user_by_id(user_id=decoded_token['user_id']) is not None:
            return callRespond(
                GroupReader.GroupReadService.read_groups_user_max_id(request.data['user_id'],
                                                                     max_id=request.data['max_id'])
            )
        else:
            return callRespond(status.HTTP_401_UNAUTHORIZED)
