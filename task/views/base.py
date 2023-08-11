from django.db import IntegrityError
from rest_framework.response import Response
from rest_framework import generics, views
from rest_framework import status

from authentication.authentication import Authentication
from authentication.permissions import IsAdmin
from common.functions import FailureSerializer
from task.services import TaskManagerService
from task.serializers import TaskSerializer, TaskUserMapSerializer

class TaskManager(generics.CreateAPIView, generics.UpdateAPIView, generics.RetrieveAPIView):
    authentication_classes = [Authentication, ]

    def get_serializer_class(self):
        return TaskSerializer

    def get(self, request, id):
        try:
            serviceInstance = TaskManagerService()
            instance = serviceInstance.get_task_by_id(id)
            serialized_data = TaskSerializer(instance=instance)
            return Response(serialized_data.data, status=status.HTTP_200_OK)
        except Exception as e:
            error = FailureSerializer().get_response(e)
            return Response(error, status=error.get("status", status.HTTP_400_BAD_REQUEST))

    def post(self, request, *args, **kwargs) -> Response:
        try:
            return super().post(request)
        except Exception as e:
            error = FailureSerializer().get_response(e)
            return Response(error, status=error.get("status", status.HTTP_400_BAD_REQUEST))
        
    def patch(self, request, *args, **kwargs):
        try:
            task_id = kwargs["id"]
            serviceInstance = TaskManagerService()
            instance = serviceInstance.get_task_by_id(task_id)
            taskInstance = serviceInstance.update_task(instance, request.data)
            serialized_data = TaskSerializer(instance=taskInstance)

            return Response(serialized_data.data, status=status.HTTP_200_OK)

        except Exception as e:
            error = FailureSerializer().get_response(e)
            return Response(error, status=error.get("status", status.HTTP_400_BAD_REQUEST))

    def delete(self, request, *args, **kwargs):
        try:
            if kwargs.get("id") is None:
                raise Exception("ID is required")

            serviceInstance = TaskManagerService()
            instance = serviceInstance.get_task_by_id(kwargs.get("id"))
            serviceInstance.delete_task(instance)

            return Response({
                "status": "SUCCESS"
            }, status=status.HTTP_200_OK)

        except Exception as e:
            error = FailureSerializer().get_response(e)
            return Response(error, status=error.get("status", status.HTTP_400_BAD_REQUEST))


class TaskListManager(generics.ListAPIView):
    authentication_classes = [Authentication, ]

    def list(self, request):
        try:
            serviceInstance = TaskManagerService()
            instance = serviceInstance.get_task_list(user=request.user)
            serialized_data = TaskSerializer(instance=instance, many=True)
            return Response(serialized_data.data)
        except Exception as e:
            error = FailureSerializer().get_response(e)
            return Response(error, status=error.get("status", status.HTTP_400_BAD_REQUEST))

class TaskOperationsManager(views.APIView):
    authentication_classes = [Authentication, ]
    permission_classes = [IsAdmin, ]

    def post(self, request):
        try:
            serialized_data = TaskUserMapSerializer(data=request.data)
            if serialized_data.is_valid(raise_exception=True):
                data = serialized_data.data
                serviceInstance = TaskManagerService()
                instance = serviceInstance.assign_task(data.get("task_id"), data.get("user_id"))
                response = TaskUserMapSerializer(instance=instance)
                return Response(response.data)

        except Exception as e:
            error = FailureSerializer().get_response(e)
            return Response(error, status=error.get("status", status.HTTP_400_BAD_REQUEST))