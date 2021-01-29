from sqlalchemy import insert, select
from modules.group.entity import GroupEntity
from http import HTTPStatus


def group_factory(name, about):
    found = (
        select(GroupEntity.Group).
        where(GroupEntity.Group.name == name).
        exists()
    )
    if not found:
        (insert(GroupEntity.Group).
         values(name=name, about=about))

        return HTTPStatus.CREATED
    else:
        return HTTPStatus.CONFLICT

