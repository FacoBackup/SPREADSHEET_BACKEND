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
        created_user = User(name=name,
                            email=email,
                            phone=phone,
                            birth=birth,
                            pic=pic,
                            about=about,
                            study=study,
                            nationality=nationality)
        created_user.save()

        group = GroupReader.GroupReadService.search_group(search_input=department)
        if group is not None:
            membership = GroupManagement.add_member(created_user.id, group_id=group.id)
            membership.save()
            return status.HTTP_201_CREATED
        else:
            return status.HTTP_201_CREATED
    except exceptions.FieldError:
        return status.HTTP_500_INTERNAL_SERVER_ERROR
    except exceptions.PermissionDenied:
        return status.HTTP_500_INTERNAL_SERVER_ERROR
