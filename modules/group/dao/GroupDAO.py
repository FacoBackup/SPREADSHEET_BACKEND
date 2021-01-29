from sqlalchemy import insert, select, and_, update, delete
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from modules.group.entity.GroupEntity import Group
from http import HTTPStatus


def check_group(group_id):
    try:
        return (select(Group).
                where(Group.id == group_id).
                exists())
    except IntegrityError:
        return False
    except SQLAlchemyError:
        return False


def create_group(name, about):
    try:
        (insert(Group).
         values(about=about, name=name))
        return HTTPStatus.CREATED
    except IntegrityError:
        return HTTPStatus.INTERNAL_SERVER_ERROR
    except SQLAlchemyError:
        return HTTPStatus.INTERNAL_SERVER_ERROR


def delete_group(group_id):
    try:
        (delete(Group).
         where(Group.id == group_id)
         )
        return HTTPStatus.OK
    except IntegrityError:
        return HTTPStatus.INTERNAL_SERVER_ERROR
    except SQLAlchemyError:
        return HTTPStatus.INTERNAL_SERVER_ERROR


def update_group(group_id, name, about):
    try:
        (update(Group).
         where(Group.id == group_id).
         values(name=name, about=about))
        return HTTPStatus.OK
    except IntegrityError:
        return HTTPStatus.INTERNAL_SERVER_ERROR
    except SQLAlchemyError:
        return HTTPStatus.INTERNAL_SERVER_ERROR
