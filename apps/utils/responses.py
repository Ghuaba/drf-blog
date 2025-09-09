from rest_framework.response import Response
from rest_framework import status

def standard_response(data=None, message="Success", code=200, http_status=status.HTTP_200_OK):
    return Response({
        "message": message,
        "code": code,
        "data": data
    }, status=http_status)
