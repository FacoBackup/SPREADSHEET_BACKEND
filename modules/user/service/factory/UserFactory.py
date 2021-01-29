from http import HTTPStatus
from modules.user.dao import UserDAO


async def user_factory(name, about, nationality, birth, study, pic, email, phone):
    found = await UserDAO.check_user_by_field(email=email, name=name, phone=phone)
    if not found:
        return await (UserDAO.create_user(name=name,
                                          about=about,
                                          phone=phone,
                                          pic=pic,
                                          email=email,
                                          birth=birth,
                                          nationality=nationality,
                                          study=study))

    else:
        return HTTPStatus.INTERNAL_SERVER_ERROR
