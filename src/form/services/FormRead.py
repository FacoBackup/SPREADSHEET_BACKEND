from src.form.models import Form, FormField, FormAccess, FormContent
from django.core import exceptions, serializers
from rest_framework import status


class FormReadService:
    @staticmethod
    def read_form_field_content(form_field_id):
        try:
            content = FormContent.objects.filter(field_fk=form_field_id)
            response = []
            for i in content:
                response.__iadd__(FormReadService.__map_content(content[i]))

            return response
        except exceptions.ObjectDoesNotExist:
            return status.HTTP_500_INTERNAL_SERVER_ERROR

    @staticmethod
    def read_form_fields(form_id):
        try:
            fields = FormField.objects.filter(form_fk=form_id)
            response = []
            for i in fields:
                response.__iadd__(FormReadService.__map_field(fields[i]))

            return response
        except exceptions.ObjectDoesNotExist:
            return status.HTTP_500_INTERNAL_SERVER_ERROR

    @staticmethod
    def read_forms_with_access(requester):
        try:
            forms = FormAccess.objects.filter(user_fk=requester)
            response = []
            for i in forms:
                response.__iadd__(FormReadService.__map_form(forms[i]))

            return response
        except exceptions.ObjectDoesNotExist:
            return status.HTTP_500_INTERNAL_SERVER_ERROR

    @staticmethod
    def read_all_content_form(form_id):
        try:
            response = []
            fields = FormField.objects.filter(form_fk=form_id)

            for i in fields:
                content = FormContent.objects.filter(field_fk=fields['id'])
                mapped_content = []
                for j in content:
                    mapped_content.__iadd__(FormReadService.__map_content(content[j]))

                response.__iadd__({
                    "field_id": fields[i].id,
                    "content": content
                })

            return response
        except exceptions.ObjectDoesNotExist:
            return status.HTTP_500_INTERNAL_SERVER_ERROR

    @staticmethod
    def __map_form(form):
        return {
            "name": form.name,
            "about": form.about,
            "group_id": form.group_fk,
            "id": form.id
        }

    @staticmethod
    def __map_field(field):
        return {
            "id": field.id,
            "form_id": field.form_fk,
            "name": field.name
        }

    @staticmethod
    def __map_content(content):
        return {
            "content": content.content,
            "id": content.id,
            "field_id": content.field_fk
        }

    @staticmethod
    def __map_access(access):
        return {
            "user_id": access.user_fk,
            "form_id": access.form_fk
        }
