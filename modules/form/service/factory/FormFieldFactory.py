# from sqlalchemy import insert, select
# from modules.form.entity import FormFieldsEntity
# from
# from http import HTTPStatus
#
#
# def form_field_factory(requester, name, about):
#     found = (
#         select(GroupEntity.Group).
#         where(GroupEntity.Group.name == name).
#         exists()
#     )
#     if not found:
#         (insert(GroupEntity.Group).
#          values(name=name, about=about))
#
#         return HTTPStatus.CREATED
#     else:
#         return HTTPStatus.CONFLICT
#
