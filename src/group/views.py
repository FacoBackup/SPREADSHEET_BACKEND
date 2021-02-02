from rest_framework.decorators import (api_view as route)
from rest_framework.response import Response as callRespond
from src.group.services import GroupFactory, GroupReader
from rest_framework.views import APIView


class GroupViews(APIView):

    @route(['POST'])
    def create_group(self, request):
        return callRespond(
            GroupFactory.create_group(name=request.data['name'],
                                      about=request.data['about'],
                                      requester=1,
                                      pic=request.data['pic'])
        )

    @route(['PATCH'])
    def get_group(self, request):
        return callRespond(
            GroupReader.GroupReadService.read_group(request.data['group_id'])
        )

    @route(['PATCH'])
    def get_groups_by_user(self, request):
        return callRespond(
            GroupReader.GroupReadService.read_groups_user(request.data['user_id'])
        )

    @route(['PATCH'])
    def get_groups_by_user_max_id(self, request):
        return callRespond(

            GroupReader.GroupReadService.read_groups_user_max_id(request.data['user_id'], max_id=request.data['max_id'])

        )
