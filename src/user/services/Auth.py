from src.user.services import UserReader
from ldap3 import Server, Connection, ALL
import jwt
import time as time_
from rest_framework import status


def sign_in(user_email, password):
    user = UserReader.UserReadService.read_user_by_email(user_email)
    if user is not None:
        # server = Server('ldap://ldap.aeb.gov.br', get_info=ALL)
        # connection = Connection(server, user=user.email, password=password)
        # if connection.bind():
        encoded_jwt = jwt.encode({"user_id": user['id'], 'exp': (time_.time() + 1000 * 60 * 10)},
                                 "askdasdiuh123i1y98yejas9d812hiu89dqw9", algorithm="HS256")
        return {
            "JWT": encoded_jwt,
            "ID": user["id"],
            "EMAIL": user["email"],
            "PHONE": user["phone"]
            }
        # else:
        #     return status.HTTP_401_UNAUTHORIZED

    else:
        return status.HTTP_401_UNAUTHORIZED
