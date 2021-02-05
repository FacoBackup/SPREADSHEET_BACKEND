from src.user.models import User
from django.core import exceptions
from rest_framework import status
from src.group.services import GroupManagement, GroupReader


def create_user(
        name,
        email,
        phone,
        about,
        birth,
        study,
        nationality,
        pic,
        department
):
    try:
        if (User.objects.filter(email=email).exists() is False) and \
                (User.objects.filter(phone=phone).exists() is False):
            created_user = User(name=name.lower(),
                                email=email.lower(),
                                phone=phone,
                                birth=birth,
                                pic=pic,
                                about=about,
                                study=study,
                                nationality=nationality)
            created_user.save()
            groups = None
            if department is not None:
                groups = GroupReader.GroupReadService.search_group(search_input=department)

            if groups:
                GroupManagement.add_member(created_user.id, group_id=groups[0]['id'])
                return status.HTTP_201_CREATED
            else:
                return status.HTTP_201_CREATED
        else:
            return status.HTTP_417_EXPECTATION_FAILED
    except exceptions.FieldError:
        return status.HTTP_500_INTERNAL_SERVER_ERROR
    except exceptions.PermissionDenied:
        return status.HTTP_500_INTERNAL_SERVER_ERROR
