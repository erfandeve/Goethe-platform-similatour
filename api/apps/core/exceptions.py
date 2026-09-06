from mongoengine.errors import DoesNotExist, NotUniqueError, ValidationError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler


class ApiError(Exception):
    def __init__(self, message, code="error", status_code=status.HTTP_400_BAD_REQUEST, fields=None):
        super().__init__(message)
        self.message = message
        self.code = code
        self.status_code = status_code
        self.fields = fields or {}


def api_exception_handler(exc, context):
    if isinstance(exc, ApiError):
        return Response(
            {"detail": exc.message, "code": exc.code, "fields": exc.fields},
            status=exc.status_code,
        )
    if isinstance(exc, DoesNotExist):
        return Response({"detail": "Not found.", "code": "not_found"}, status=404)
    if isinstance(exc, NotUniqueError):
        return Response({"detail": "Duplicate value.", "code": "duplicate"}, status=409)
    if isinstance(exc, ValidationError):
        return Response({"detail": str(exc), "code": "invalid"}, status=400)
    return exception_handler(exc, context)
