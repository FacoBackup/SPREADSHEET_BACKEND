from src.user.models import User
from django.core import exceptions, serializers


def read_user_by_id(user_id):
    try:
        user_query = User.objects.filter(id=user_id)
        if user_query is not None:
            query = serializers.serialize("json", user_query)

            return query
        else:
            return 500
    except exceptions.ObjectDoesNotExist:
        return 500


def read_all_users():
    try:
        user_query = User.objects.all()
        if user_query is not None:
            query = serializers.serialize("json", user_query)

            return query
        else:
            return 500

    except exceptions.ObjectDoesNotExist:
        return 500


def read_user_by_max_id(max_id):
    try:
        user_query = User.objects.filter(id__lt=max_id)
        if user_query is not None:
            query = serializers.serialize("json", user_query)

            return query
        else:
            return 500

    except exceptions.ObjectDoesNotExist:
        return 500


def read_users():
    try:
        user_query = User.objects.order_by('-id').all()[:10]
        if user_query is not None:
            query = serializers.serialize("json", user_query)

            return query
        else:
            return 500

    except exceptions.ObjectDoesNotExist:
        return 500
