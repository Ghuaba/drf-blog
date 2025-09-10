from rest_framework.response import Response
from rest_framework import status
from rest_framework.utils.serializer_helpers import ReturnList

def standard_response(data=None, message="Success", code=0, http_status=status.HTTP_200_OK):
    """
        "success": bool,   # True si http_status está entre 200–299, False de lo contrrario
        "message": str,    # Mensaje enviado por la API
        "code": int,       # Código interno definido por la API, personalizado
        "status": int,     # Código HTTP real
        "data": object     # Cuando es un único objeto
        "results": list,   # Cuando es lista o paginación
        "count": int,      # Total de elementos (si aplica, listas/paginación)
        "next": str|null,  # URL siguiente página (si es paginación DRF)
        "previous": str|null # URL página previa (si es paginación DRF)
    """
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
