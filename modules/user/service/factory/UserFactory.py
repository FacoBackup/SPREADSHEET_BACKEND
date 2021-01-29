from sqlalchemy import insert, select, or_
from modules.user.entity import UserEntity
from http import HTTPStatus


def user_factory(name, about, nationality, birth, study, pic, email, phone):
    found = (
        select(UserEntity.User).
        where(or_(UserEntity.User.name == name, UserEntity.User.phone == phone, UserEntity.User.email == email)).
        exists()
    )
    if not found:
        (insert(UserEntity.User).
         values(name=name,
                about=about,
                phone=phone,
                pic=pic,
                email=email,
                birth=birth,
                nationality=nationality,
                study=study))

        return HTTPStatus.CREATED
    else:
        return HTTPStatus.CONFLICT

