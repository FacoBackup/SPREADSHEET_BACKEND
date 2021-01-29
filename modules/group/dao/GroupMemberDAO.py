from sqlalchemy import insert, select, and_, update, delete
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from modules.group.entity.GroupMemberEntity import GroupMember
from http import HTTPStatus


def check_group_member(group_member_id, group_id):
    try:
        return (select(GroupMember).
                where(and_(GroupMember.user_fk == group_member_id, GroupMember.group_fk == group_id)).
                exists())
    except IntegrityError:
        return False
    except SQLAlchemyError:
        return False


def create_group_member(role, user_id, group_id):
    try:
        (insert(GroupMember).
         values(role=role, group_fk=group_id, user_fk=user_id))
        return HTTPStatus.CREATED
    except IntegrityError:
        return HTTPStatus.INTERNAL_SERVER_ERROR
    except SQLAlchemyError:
        return HTTPStatus.INTERNAL_SERVER_ERROR


def delete_group_member(group_member_id):
    try:
        (delete(GroupMember).
         where(GroupMember.user_fk == group_member_id)
         )
        return HTTPStatus.OK
    except IntegrityError:
        return HTTPStatus.INTERNAL_SERVER_ERROR
    except SQLAlchemyError:
        return HTTPStatus.INTERNAL_SERVER_ERROR


def update_group_member(group_member_id, role):
    try:
        (update(GroupMember).
         where(GroupMember.user_fk == group_member_id).
         values(role=role))
        return HTTPStatus.OK
    except IntegrityError:
        return HTTPStatus.INTERNAL_SERVER_ERROR
    except SQLAlchemyError:
        return HTTPStatus.INTERNAL_SERVER_ERROR


def read_members_by_max_id(group_id, max_id):
    try:
        return (select(GroupMember).
                where(and_(GroupMember.group_fk == group_id, GroupMember.user_fk.in_([max_id, (max_id - 5)]))).
                limit())
    except IntegrityError:
        return None
    except SQLAlchemyError:
        return None


def read_all_group_members(group_id):
    try:
        return select(GroupMember).where(GroupMember.group_fk == group_id).all()
    except IntegrityError:
        return None
    except SQLAlchemyError:
        return None
