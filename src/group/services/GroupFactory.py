from src.group.models import GroupMembership, Group
from django.core import exceptions
from rest_framework import status


def create_group(name, about, pic):
    try:
        name = (name.lower()).replace(" ", "")
        group_id = Group(name=name, about=about, pic=pic, tag=name)
        group_id.save()

        return status.HTTP_201_CREATED
    except exceptions.FieldError:
        return status.HTTP_500_INTERNAL_SERVER_ERROR
    except exceptions.PermissionDenied:
        return status.HTTP_500_INTERNAL_SERVER_ERROR
