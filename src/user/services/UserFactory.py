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
            group = None
            if department is not None:
                group = GroupReader.GroupReadService.read_group_by_name(name=department)

            if group is not None:
                GroupManagement.add_member(created_user.id, group_id=group[0]['id'])
                return status.HTTP_201_CREATED
            else:
                return status.HTTP_201_CREATED
        else:
            return status.HTTP_417_EXPECTATION_FAILED
    except exceptions.FieldError:
        return status.HTTP_500_INTERNAL_SERVER_ERROR
    except exceptions.PermissionDenied:
        return status.HTTP_500_INTERNAL_SERVER_ERROR


def update_profile(user_id, phone, pic, background, about, study):
    user = User.objects.get(id=user_id)
    if user is not None:
        if phone is not None:
            user.phone = phone
        if pic is not None:
            user.pic = pic
        if background is not None:
            user.background = background
        if about is not None:
            user.about = about
        if study is not None:
            user.study = study
        user.save()
        return status.HTTP_200_OK
    else:
        return status.HTTP_404_NOT_FOUND
