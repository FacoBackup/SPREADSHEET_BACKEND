from django.core import exceptions

from src.group.models import GroupMembership


def promote_member(member_id, group_id):
    try:
        group_membership = GroupMembership.objects.filter(user_fk=member_id, group_fk=group_id).first()
        if group_membership.role != 'ADMIN':
            group_membership.role = 'ADMIN'
            group_membership.save()
    except exceptions.ObjectDoesNotExist:
        return 500


def lower_member(member_id, group_id):
    try:
        group_membership = GroupMembership.objects.filter(user_fk=member_id, group_fk=group_id).first()
        if group_membership.role == 'ADMIN':
            group_membership.role = 'MEMBER'
            group_membership.save()
    except exceptions.ObjectDoesNotExist:
        return 500


def add_member(member_id, group_id):
    try:
        group_membership = GroupMembership(user_fk=member_id, group_fk=group_id, role="MEMBER")
        group_membership.save()
    except exceptions.ObjectDoesNotExist:
        return 500


def remove_member(member_id, group_id):
    try:
        group_membership = GroupMembership.objects.get(user_fk=member_id, group_fk=group_id)
        group_membership.delete()
    except exceptions.ObjectDoesNotExist:
        return 500
