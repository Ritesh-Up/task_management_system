from rest_framework.response import Response
from rest_framework import generics, views
from rest_framework import status

from user.models import UserModel
from common.functions import FailureSerializer
from authentication.authentication import Authentication
from user.serializers import UserSerializer

class UserView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        try:
            instance = UserModel.objects.create(
                name=request.data.get("name"),
                email=request.data.get("email")
            )
            serialized_data = UserSerializer(instance=instance)
            return Response(serialized_data.data)
        except Exception as e:
            error = FailureSerializer().get_response(e)
            return Response(error, status=error.get("status", status.HTTP_400_BAD_REQUEST))
