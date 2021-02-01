from src.form.models import Form, FormField, FormAccess, FormContent
from django.core import exceptions, serializers
from rest_framework import status


def read_form_field_content(form_field_id):
    try:
        content = FormContent.objects.filter(field_fk=form_field_id)

        return serializers.serialize("json", content)
    except exceptions.ObjectDoesNotExist:
        return status.HTTP_500_INTERNAL_SERVER_ERROR


def read_form_fields(form_id):
    try:
        fields = FormField.objects.filter(form_fk=form_id)

        return serializers.serialize("json", fields)
    except exceptions.ObjectDoesNotExist:
        return status.HTTP_500_INTERNAL_SERVER_ERROR


def read_forms_with_access(requester):
    try:
        forms = FormAccess.objects.filter(user_fk=requester)


        # return serializers.serialize("json", fields)
    except exceptions.ObjectDoesNotExist:
        return status.HTTP_500_INTERNAL_SERVER_ERROR


def read_all_content_form(form_id):
    print("OK")
