from rest_framework.response import Response
from rest_framework import generics, views
from rest_framework import status
import jwt

from user.serializers import UserSerializer
from user.models import UserModel
from common.functions import FailureSerializer

class Auth(generics.RetrieveAPIView):

    def get(self, request, id):
        try:
            user_object = UserModel.objects.get(id=id)
            serialized_data = UserSerializer(instance=user_object)
            token = jwt.encode({"payload": serialized_data.data}, "secret", algorithm="HS256")
            return Response(token)
        except UserModel.DoesNotExist:
            error = FailureSerializer().get_response("User doesn't exist")
            return Response(error, status=error.get("status", status.HTTP_400_BAD_REQUEST))
        except Exception as e:
            error = FailureSerializer().get_response(e)
            return Response(error, status=error.get("status", status.HTTP_400_BAD_REQUEST))

