from rest_framework_simplejwt.tokens import AccessToken
from src.user.services import UserRead
import json
import jwt
import time as time_
from rest_framework import status


def sign_in(user_field):
    found = UserRead.search_user(user_field)
    if found is not None:

        user = json.loads(found)
        email = user[0]['fields']['email']
        encoded_jwt = jwt.encode({"user_email": email, 'exp': (time_.time()) + 1000 * 60 * 10},
                                 "askdasdiuh123i1y98yejas9d812hiu89dqw9", algorithm="HS256")

        return encoded_jwt

    else:
        return status.HTTP_404_NOT_FOUND
