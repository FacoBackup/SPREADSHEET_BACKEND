from django.core import exceptions
from rest_framework import status
from src.group.models import GroupMembership, Group
from src.user.models import User


#
# def promote_member(member_id, group_id):
#     try:
#         group_membership = GroupMembership.objects.filter(user_fk=member_id, group_fk=group_id).first()
#         if group_membership.role != 'ADMIN':
#             group_membership.role = 'ADMIN'
#             group_membership.save()
#     except exceptions.ObjectDoesNotExist:
#         return status.HTTP_500_INTERNAL_SERVER_ERROR
#
#
# def lower_member(member_id, group_id):
#     try:
#         group_membership = GroupMembership.objects.filter(user_fk=member_id, group_fk=group_id).first()
#         if group_membership.role == 'ADMIN':
#             group_membership.role = 'MEMBER'
#             group_membership.save()
#     except exceptions.ObjectDoesNotExist:
#         return status.HTTP_500_INTERNAL_SERVER_ERROR
#

def add_member(member_id, group_id):
    try:
        user = User.objects.get(id=member_id)
        group = Group.objects.get(id=group_id)
        if user is not None and group is not None:
            group_membership = GroupMembership(user_fk=user, group_fk=group, role="MEMBER")
            group_membership.save()
            return status.HTTP_200_OK
        else:
            return status.HTTP_500_INTERNAL_SERVER_ERROR
    except exceptions.ObjectDoesNotExist:
        return status.HTTP_500_INTERNAL_SERVER_ERROR


def remove_member(member_id, group_id):
    try:
        group_membership = GroupMembership.objects.get(user_fk=member_id, group_fk=group_id)
        group_membership.delete()
        return status.HTTP_200_OK
    except exceptions.ObjectDoesNotExist:
        return status.HTTP_500_INTERNAL_SERVER_ERROR
