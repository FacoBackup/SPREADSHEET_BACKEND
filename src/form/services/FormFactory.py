from rest_framework import status
from src.user.models import User
from django.core import exceptions
from src.form.models import Form, FormField, FormAccess, FormContent


def create_form(name, about, group_id, requester):
    try:
        form = Form(name=name, about=about, group_fk=group_id)
        form.save()
        form_access = FormAccess(user_fk=requester, form_fk=form)
        form_access.save()

        return status.HTTP_201_CREATED
    except exceptions.FieldError:
        return status.HTTP_500_INTERNAL_SERVER_ERROR
    except exceptions.PermissionDenied:
        return status.HTTP_500_INTERNAL_SERVER_ERROR


def create_form_field(form_id, name):
    try:
        form_field = FormField(name=name, form_fk=form_id)
        form_field.save()

        return status.HTTP_201_CREATED
    except exceptions.FieldError:
        return status.HTTP_500_INTERNAL_SERVER_ERROR
    except exceptions.PermissionDenied:
        return status.HTTP_500_INTERNAL_SERVER_ERROR


def create_form_field_content(content, form_field_id, requester):
    try:
        form_content = FormContent(content=content, creator=requester, form_fk=form_field_id)
        form_content.save()
        return status.HTTP_201_CREATED
    except exceptions.FieldError:
        return status.HTTP_500_INTERNAL_SERVER_ERROR
    except exceptions.PermissionDenied:
        return status.HTTP_500_INTERNAL_SERVER_ERROR


def create_form_access(user_id, form_id):
    try:

        form_access = FormAccess(user_fk=user_id, form_fk=form_id)
        form_access.save()
        return status.HTTP_201_CREATED
    except exceptions.FieldError:
        return status.HTTP_500_INTERNAL_SERVER_ERROR
    except exceptions.PermissionDenied:
        return status.HTTP_500_INTERNAL_SERVER_ERROR
