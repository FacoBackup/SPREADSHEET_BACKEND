from src.user.models import User
from django.core import exceptions, serializers
from django.db.models import Q


def search_user(search_input):
    try:
        user_query = User.objects.filter(Q(name=search_input) | Q(email=search_input))
        if user_query is not None:
            query = serializers.serialize("json", user_query)

            return query
        else:
            return 500
    except exceptions.ObjectDoesNotExist:
        return 500


def read_user_by_email(email):
    try:
        user_query = User.objects.get(email=email)
        if user_query is not None:
            query = serializers.serialize("json", [user_query])

            return query
        else:
            return None
    except exceptions.ObjectDoesNotExist:
        return None


def read_user_by_id(user_id):
    try:
        user_query = User.objects.get(id=user_id)
        print(user_query)
        if user_query is not None:
            query = serializers.serialize("json", [user_query])
            print(query)
            return query
        else:
            print("RETURNING NONE")
            return None
    except exceptions.ObjectDoesNotExist:
        print("RETURNING NONE")
        return None


def read_all_users():
    try:
        user_query = User.objects.all()
        if user_query:
            query = serializers.serialize("json", user_query)

            return query
        else:
            return 500

    except exceptions.ObjectDoesNotExist:
        return 500


def read_user_by_max_id(max_id):
    try:
        user_query = User.objects.filter(id__lt=max_id)
        if user_query:
            query = serializers.serialize("json", user_query)

            return query
        else:
            return 500

    except exceptions.ObjectDoesNotExist:
        return 500


def read_users():
    try:
        user_query = User.objects.order_by('-id').all()[:10]
        test = []
        if test:
            print("Empty")
        else:
            print("is not empty ")
        return serializers.serialize("json", user_query)

    except exceptions.ObjectDoesNotExist:
        return 500
