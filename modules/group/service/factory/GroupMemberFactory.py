from sqlalchemy import insert, select
from modules.group.entity import GroupMemberEntity
from http import HTTPStatus


def group_member_factory(user_id, group_id, role):
    found = (
        select(GroupMemberEntity.GroupMember).
        where(GroupMemberEntity.GroupMember.user_fk == user_id).
        exists()
    )
    if not found:
        (
            insert(GroupMemberEntity.GroupMember).
            values(user_fk=user_id, group_fk=group_id, role=role)
        )
        return HTTPStatus.CREATED
    else:
        return HTTPStatus.CONFLICT


d