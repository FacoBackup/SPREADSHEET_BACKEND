from src.group.models import Group, GroupMembership
from rest_framework import status
from django.core import exceptions, serializers


class GroupReadService:

    @staticmethod
    def verify_member(user_id, group_id):
        try:
            member = GroupMembership.objects.get(group_fk=group_id, user_fk=user_id)

            if member is not None:
                return True
            else:
                return False
        except exceptions.ObjectDoesNotExist:
            return False

    @staticmethod
    def read_first_group(user_id):
        try:
            member = GroupMembership.objects.filter(user_fk=user_id)[:1]
            if len(member) > 0:
                return GroupReadService.__map_membership(member[0])
            else:
                return None
        except exceptions.ObjectDoesNotExist:
            return None

    @staticmethod
    def search_group(search_input):
        try:
            tag = (search_input.lower()).replace(" ", "")
            group_query = Group.objects.filter(tag__contains=tag)
            response = []
            for i in group_query:
                response.append(GroupReadService.__map_group(i))

            return response
        except exceptions.ObjectDoesNotExist:
            return None

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
            memberships = (
                GroupMembership.objects.filter(user_fk=user_id).select_related()[:10]
            )

            groups = []

            for i in memberships:
                membership = GroupReadService.__map_membership(i)
                group = Group.objects.get(id=membership['group_id'])
                if group is not None:
                    groups.append(GroupReadService.__map_group(group))

            return groups
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
                response.append(GroupReadService.__map_membership(i))

            return response

        except exceptions.ObjectDoesNotExist:
            return status.HTTP_500_INTERNAL_SERVER_ERROR

    @staticmethod
    def __map_membership(membership):
        return {
            "user_id": membership.user_fk.id,
            "group_id": membership.group_fk.id,
            "role": membership.role
        }

    @staticmethod
    def __map_group(group):
        return {
            "name": group.name,
            "about": group.about,
            "id": group.id,
            "pic": group.pic
        }
