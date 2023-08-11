from rest_framework import authentication, exceptions
import jwt
from user.models import UserModel

class Authentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        if "Authorization" in request.headers and request.headers["Authorization"] is not None:
            try:
                data = jwt.decode(jwt=request.headers["Authorization"], key='secret', algorithms=["HS256"])
                user = UserModel.objects.get(id=data.get("payload").get("id"))
                request.user = user
                print("User:", request.user.user_role)
                return (request.user, None)
            except:
                raise exceptions.AuthenticationFailed("Authentication Failed")

        raise exceptions.AuthenticationFailed("Authentication Failed")