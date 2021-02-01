from rest_framework_simplejwt.tokens import RefreshToken
from src.user.services import UserRead
import json

def sign_in(user_field):
    found = UserRead.search_user(user_field)
    if found is not None:

        user = json.loads(found)

        if user:
            email = user[0]['fields']['email']

            refresh = RefreshToken.for_user(user[0]['fields'])

            return {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        else:
            return 500
    else:
        return 500