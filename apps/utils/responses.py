from rest_framework.response import Response
from rest_framework import status
from rest_framework.utils.serializer_helpers import ReturnList

def standard_response(data=None, message="Success", code=0, http_status=status.HTTP_200_OK):
    success = 200 <= http_status < 300

    # Detectar si data es paginación DRF
    if isinstance(data, dict) and "results" in data:
        payload = data  # mantiene count, next, previous, results
    elif isinstance(data, list):
        payload = {"results": data, "count": len(data)}
    else:
        payload = {"data": data}

    return Response({
        "success": success,
        "message": message,
        "code": code,
        "status": http_status,
        **payload
    }, status=http_status)