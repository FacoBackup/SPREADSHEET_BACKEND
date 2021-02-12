from src.group.models import Group, GroupMembership
from rest_framework import status
from django.core import exceptions
from src.user.services import UserReader
from src.file_management.services.repository import RepositoryReader


class GroupReadService:
    @staticmethod
    def read_group_members(group_id):
        try:
            members = GroupMembership.objects.filter(group_fk=group_id)
            response = []
            for i in members:
                response.append(UserReader.UserReadService.map_user(i.user_fk, group_id=i.group_fk.id))
            return response
        except exceptions.ObjectDoesNotExist:
            return []

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
            if group_query is not None:
                members = len(GroupReadService.read_group_members(group_id=group_query.id))
                repositories = len(
                    RepositoryReader.RepositoryReadService.read_group_repositories(group_id=group_query.id))
                return {
                    "group": GroupReadService.__map_group(group_query),
                    "repositories": repositories,
                    "members": members
                }
            else:
                return None
        except exceptions.ObjectDoesNotExist:
            return None

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
