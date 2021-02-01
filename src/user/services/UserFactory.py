from src.user.models import User
from django.core import exceptions
from rest_framework import status


def create_user(
        name,
        email,
        phone,
        about,
        birth,
        study,
        nationality,
        pic):
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
        return status.HTTP_201_CREATED
    except exceptions.FieldError:
        return status.HTTP_500_INTERNAL_SERVER_ERROR
    except exceptions.PermissionDenied:
        return status.HTTP_500_INTERNAL_SERVER_ERROR
