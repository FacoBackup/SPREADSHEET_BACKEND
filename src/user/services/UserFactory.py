from src.user.models import User
from django.core import exceptions


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
        return 201
    except exceptions.FieldError:
        return 500
    except exceptions.PermissionDenied:
        return 500
