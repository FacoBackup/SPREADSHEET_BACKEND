from src.group.models import Group, GroupMembership
from rest_framework import status
from django.core import exceptions, serializers


class GroupReadService:
    @staticmethod
    def search_group(search_input):
        try:
            group_query = Group.objects.filter(name=search_input)

            response = []
            for i in group_query:
                response.__iadd__(GroupReadService.__map_group(group_query[i]))

            return response
        except exceptions.ObjectDoesNotExist:
            return status.HTTP_500_INTERNAL_SERVER_ERROR

    @staticmethod
    def read_group(group_id):
        try:
            group_query = Group.objects.get(id=group_id)

            return GroupReadService.__map_group(group_query)
        except exceptions.ObjectDoesNotExist:
            return status.HTTP_500_INTERNAL_SERVER_ERROR

    @staticmethod
    def read_groups_user(user_id):
        try:
            group_query = (
                GroupMembership.objects.filter(user_fk=user_id).select_related()[:10]
            )

            response = []
            for i in group_query:
                response.__iadd__(GroupReadService.__map_group(group_query[i]))

            return response
        except exceptions.ObjectDoesNotExist:
            return status.HTTP_500_INTERNAL_SERVER_ERROR

    @staticmethod
    def read_groups_user_max_id(user_id, max_id):
        try:
            group_query = (
                GroupMembership.objects.filter(user_fk=user_id, group_fk__lt=max_id).select_related()[:10]
            )

            response = []
            for i in group_query:
                response.__iadd__(GroupReadService.__map_group(group_query[i]))

            return response

        except exceptions.ObjectDoesNotExist:
            return status.HTTP_500_INTERNAL_SERVER_ERROR

    @staticmethod
    def __map_group(group):
        return {
            "name": group.name,
            "about": group.about,
            "id": group.id,
            "pic": group.pic
        }
