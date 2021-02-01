from src.group.models import GroupMembership, Group
from src.user.models import User
from django.core import exceptions, serializers


def create_group(name, about, pic, requester):
    try:
        group_id = Group(name=name, about=about, pic=pic)
        group_id.save()
        group_membership = GroupMembership(user_fk=requester, group_fk=group_id, role="MEMBER")
        group_membership.save()
        return 201
    except exceptions.ObjectDoesNotExist:
        return 500
