from src.user.models import User
from django.core import exceptions, serializers
from django.db.models import Q
from rest_framework import status


class UserReadService:

    @staticmethod
    def search_user(search_input):
        try:
            user_query = User.objects.filter(Q(name=search_input) | Q(email=search_input))
            response = []
            for i in user_query:
                response.__iadd__(UserReadService.__map_user(user_query[i]))
            return response
        except exceptions.ObjectDoesNotExist:
            return status.HTTP_500_INTERNAL_SERVER_ERROR

    @staticmethod
    def read_user_by_email(email):
        try:
            user_query = User.objects.get(email=email)
            if user_query is not None:
                return UserReadService.__map_user(user_query)
        except exceptions.ObjectDoesNotExist:
            return None
        except exceptions.FieldError:
            return None

    @staticmethod
    def read_user_by_id(user_id):
        try:
            user_query = User.objects.get(id=user_id)

            return UserReadService.__map_user(user_query)
        except exceptions.ObjectDoesNotExist:
            return None

    @staticmethod
    def read_all_users():
        try:
            user_query = User.objects.all()
            response = []
            for i in user_query:
                response.__iadd__(UserReadService.__map_user(user_query[i]))
            return response

        except exceptions.ObjectDoesNotExist:
            return status.HTTP_500_INTERNAL_SERVER_ERROR

    @staticmethod
    def read_user_by_max_id(max_id):
        try:
            user_query = User.objects.filter(id__lt=max_id)
            response = []
            for i in user_query:
                response.__iadd__(UserReadService.__map_user(user_query[i]))
            return response
        except exceptions.ObjectDoesNotExist:
            return status.HTTP_500_INTERNAL_SERVER_ERROR

    @staticmethod
    def read_users():
        try:
            user_query = User.objects.order_by('-id').all()[:10]
            response = []
            for i in user_query:
                response.__iadd__(UserReadService.__map_user(user_query[i]))
            return response

        except exceptions.ObjectDoesNotExist:
            return status.HTTP_500_INTERNAL_SERVER_ERROR

    @staticmethod
    def __map_user(user):
        return {
            'id': user.id,
            'name': user.name,
            'about': user.about,
            'birth': user.birth,
            'nationality': user.nationality,
            'email': user.email,
            'phone': user.phone,
            'pic': user.pic,
            'study': user.study
        }
