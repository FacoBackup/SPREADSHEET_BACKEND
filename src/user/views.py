import json
from django.http import response
from rest_framework import status
from rest_framework.decorators import (api_view as route)
from rest_framework.response import Response as callRespond
from src.user.services import UserRead, UserFactory
from src.user.services import Auth
from rest_framework.views import APIView


class UserViews(APIView):

    @route(['POST'])
    def create_user(self, request):
        return callRespond(UserFactory.create_user(nationality=request.data['nationality'],
                                                   name=request.data['name'],
                                                   email=request.data['email'],
                                                   about=request.data['about'],
                                                   phone=request.data['phone'],
                                                   pic=request.data['pic'],
                                                   study=request.data['study'],
                                                   birth=request.data['birth']))

    @route(['PATCH'])
    def get_user_by_id(self, request):
        data = UserRead.UserReadService.read_user_by_id(request.data['id'])
        if data is not None:
            return callRespond(data)
        else:
            print("404 error")
            return callRespond(status.HTTP_404_NOT_FOUND)

    @route(['PATCH'])
    def get_user_by_max_id(self, request):
        data = UserRead.UserReadService.read_user_by_max_id(request.data['max_id'])
        if data is not None:
            return callRespond(data)
        else:
            return callRespond(status.HTTP_404_NOT_FOUND)

    @route(['GET'])
    def get_users(self, request):
        return callRespond(UserRead.UserReadService.read_users())

    @route(['POST'])
    def sign_in(self, request):
        return callRespond(Auth.sign_in(request.data['email']))
