from rest_framework import serializers
from rest_framework import status as http_status
from rest_framework.utils.serializer_helpers import ReturnDict


class FailureSerializer(serializers.Serializer):
    """Serialize to handle failure responses.
    """
    status = http_status.HTTP_400_BAD_REQUEST
    error = "Bad Request"
    message = "Something went wrong!"

    def get_response(self, exception, data: dict = {}) -> dict:
        """Overridden method to return failure message.

        Args:
            data: Key value pair of fields required.
        """
        error_detail = {}
        if hasattr(exception, "items"):
            for field_name, field_errors in exception.items():
                error_detail[field_name] =  field_errors[0] if len(field_errors) > 0 else str(field_errors)
        elif hasattr(exception, "args") and len(exception.args) > 0:
            for item in exception.args:
                if type(item) == ReturnDict:
                    for field_name in item:
                        error_detail[field_name] =  item[field_name][0] if len(item[field_name]) > 0 else str(item[field_name])
                elif type(item) == dict:
                    for field in item:
                        error_detail[field] = item[field]
                else:
                    error_detail = str(item)
        else:
            error_detail = str(exception)

        self.status = http_status.HTTP_400_BAD_REQUEST

        if hasattr(exception, "status_code"):
            self.status = exception.status_code

        response = {
            "status": data.get("status", self.status),
            "error": data.get("error", self.error),
            "message": data.get("message", self.message),
            "detail": error_detail
        }
        return response