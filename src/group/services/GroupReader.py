from src.group.models import Group, GroupMembership
from src.user.models import User
from django.core import exceptions, serializers


def search_group(search_input):
    try:
        group_query = Group.objects.filter(name=search_input)
        if group_query is not None:
            query = serializers.serialize("json", group_query)

            return query
        else:
            return 500

    except exceptions.ObjectDoesNotExist:
        return 500


def read_group(group_id):
    try:
        group_query = Group.objects.get(id=group_id)
        if group_query is not None:
            query = serializers.serialize("json", group_query)

            return query
        else:
            return 500

    except exceptions.ObjectDoesNotExist:
        return 500


def read_groups_user(user_id):
    try:
        group_query = (
            GroupMembership.objects.filter(user_fk=user_id).select_related()[:10]
        )
        if group_query is not None:
            query = serializers.serialize("json", group_query)

            return query
        else:
            return 500

    except exceptions.ObjectDoesNotExist:
        return 500


def read_groups_user_max_id(user_id, max_id):
    try:
        group_query = (
            GroupMembership.objects.filter(user_fk=user_id, group_fk__lt=max_id).select_related()[:10]
        )

        if group_query is not None:
            query = serializers.serialize("json", group_query)

            return query
        else:
            return 500

    except exceptions.ObjectDoesNotExist:
        return 500
