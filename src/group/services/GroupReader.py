from src.group.models import Group
from src.group_management.models import GroupMembership
from src.user.models import User
from django.core import exceptions, serializers


def read_group(group_id):
    try:
        group_query = Group.objects.filter(id=group_id)
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
            Group.objects.select_related(User, GroupMembership).
            filter(user_fk=user_id, id=GroupMembership.group_fk).
            all()[:10]
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
            Group.objects.select_related(User, GroupMembership).
            filter(id__lt=max_id, user_fk=user_id, id=GroupMembership.group_fk).
            all()[:10]
        )

        if group_query is not None:
            query = serializers.serialize("json", group_query)

            return query
        else:
            return 500

    except exceptions.ObjectDoesNotExist:
        return 500
