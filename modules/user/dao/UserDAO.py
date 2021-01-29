from sqlalchemy import insert, select, or_, update, delete
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from modules.user.entity.UserEntity import User
from http import HTTPStatus


async def check_user(user_id):
    try:
        return await select(User).where(User.id == user_id).exists()
    except IntegrityError:
        return False
    except SQLAlchemyError:
        return False


async def check_user_by_field(email, name, phone):
    try:
        query = await select(User).where(or_(User.name == name, User.phone == phone, User.email == email)).exists()
        if query:
            return True
        else:
            return False

    except IntegrityError:
        return False
    except SQLAlchemyError:
        return False


def read_user(user_id):
    try:
        print(user_id)
        return select(User).where(User.id == user_id).first()
    except IntegrityError:
        return None
    except SQLAlchemyError:
        return None


async def search_user(search_input):
    try:
        return await select(User).where(
            or_(User.email.like(search_input), User.name.like(search_input)))
    except IntegrityError:
        return None
    except SQLAlchemyError:
        return None


async def create_user(name, about, nationality, birth, pic, phone, email, study):
    try:
        await (insert(User).
               values(name=name,
                      about=about,
                      phone=phone,
                      pic=pic,
                      email=email,
                      birth=birth,
                      nationality=nationality,
                      study=study))
        return HTTPStatus.CREATED
    except IntegrityError:
        return HTTPStatus.INTERNAL_SERVER_ERROR
    except SQLAlchemyError:
        return HTTPStatus.INTERNAL_SERVER_ERROR


async def delete_user(user_id):
    try:
        await(delete(User).
              where(User.id == user_id)
              )
        return HTTPStatus.OK
    except IntegrityError:
        return HTTPStatus.INTERNAL_SERVER_ERROR
    except SQLAlchemyError:
        return HTTPStatus.INTERNAL_SERVER_ERROR


async def update_user(user_id, name, about, nationality, birth, pic, phone, email, study):
    try:
        await(update(User).
              where(User.id == user_id).
              values(name=name,
                     about=about,
                     phone=phone,
                     pic=pic,
                     email=email,
                     birth=birth,
                     nationality=nationality,
                     study=study))
        return HTTPStatus.OK
    except IntegrityError:
        return HTTPStatus.INTERNAL_SERVER_ERROR
    except SQLAlchemyError:
        return HTTPStatus.INTERNAL_SERVER_ERROR


async def read_all_users():
    try:
        return await select(User).all()
    except IntegrityError:
        return None
    except SQLAlchemyError:
        return None
