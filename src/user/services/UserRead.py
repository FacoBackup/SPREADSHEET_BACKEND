from django.db.models import Q

from src.user.models import User
from django.core import exceptions, serializers
from rest_framework import status
from src.group.services.GroupReader import GroupReadService


class UserReadService:

    @staticmethod
    def search_user(search_input):
        try:
            print("HERE")
            print(search_input)
            user_query = User.objects.filter(Q(name__contains=search_input) | Q(email__contains=search_input))
            response = []
            for i in user_query:
                group = GroupReadService.read_first_group(user_id=i.id)
                if group is not None:
                    response.append(UserReadService.__map_user(i, group_id=group['group_id']))
                else:
                    response.append(UserReadService.__map_user(i, group_id=None))
            return response
        except exceptions.ObjectDoesNotExist:
            return status.HTTP_500_INTERNAL_SERVER_ERROR

    @staticmethod
    def read_user_by_email(email):
        try:
            user_query = User.objects.get(email=email)
            if user_query is not None:
                return UserReadService.__map_user(user_query, None)
        except exceptions.ObjectDoesNotExist:
            return None
        except exceptions.FieldError:
            return None

    @staticmethod
    def read_user_by_id(user_id):
        try:
            user_query = User.objects.get(id=user_id)
            group = GroupReadService.read_first_group(user_id=user_id)
            if group is not None:
                return UserReadService.__map_user(user_query, group['group_id'])
            else:
                return UserReadService.__map_user(user_query, None)
        except exceptions.ObjectDoesNotExist:
            return None

    @staticmethod
    def read_all_users():
        try:
            user_query = User.objects.all()
            response = []
            for i in user_query:
                group = GroupReadService.read_first_group(user_id=i.id)
                if group is not None:
                    response.append(UserReadService.__map_user(i, group_id=group['group_id']))
                else:
                    response.append(UserReadService.__map_user(i, group_id=None))
            return response

        except exceptions.ObjectDoesNotExist:
            return status.HTTP_500_INTERNAL_SERVER_ERROR

    @staticmethod
    def read_user_by_max_id(max_id):
        try:
            user_query = User.objects.filter(id__lt=max_id)
            response = []
            for i in user_query:
                group = GroupReadService.read_first_group(user_id=i.id)
                if group is not None:
                    response.append(UserReadService.__map_user(i, group_id=group['group_id']))
                else:
                    response.append(UserReadService.__map_user(i, group_id=None))
            return response
        except exceptions.ObjectDoesNotExist:
            return status.HTTP_500_INTERNAL_SERVER_ERROR

    @staticmethod
    def read_users():
        try:
            user_query = User.objects.order_by('-id').all()[:10]
            response = []
            for i in user_query:
                group = GroupReadService.read_first_group(user_id=i.id)
                if group is not None:
                    response.append(UserReadService.__map_user(i, group_id=group['group_id']))
                else:
                    response.append(UserReadService.__map_user(i, group_id=None))
            return response

        except exceptions.ObjectDoesNotExist:
            return status.HTTP_500_INTERNAL_SERVER_ERROR

    @staticmethod
    def __map_user(user, group_id):
        return {
            'id': user.id,
            'name': user.name,
            'about': user.about,
            'birth': user.birth,
            'nationality': user.nationality,
            'email': user.email,
            'phone': user.phone,
            'pic': user.pic,
            'background': user.background,
            'study': user.study,
            'group_id': group_id
        }
