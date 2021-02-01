from src.group.models import GroupMembership, Group
from django.core import exceptions, serializers
from rest_framework import status


def create_group(name, about, pic, requester):
    try:
        group_id = Group(name=name, about=about, pic=pic)
        group_id.save()
        group_membership = GroupMembership(user_fk=requester, group_fk=group_id, role="MEMBER")
        group_membership.save()
        return status.HTTP_201_CREATED
    except exceptions.FieldError:
        return status.HTTP_500_INTERNAL_SERVER_ERROR
    except exceptions.PermissionDenied:
        return status.HTTP_500_INTERNAL_SERVER_ERROR
