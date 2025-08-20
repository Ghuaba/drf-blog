from rest_framework.views import APIView
from rest_framework.response import Response

class TestView(APIView):
    """
    A simple API view to handle tasks.
    """
    #Basic view to test boilerplate configuration
    def get(self, request, *args, **kwargs):
        """
        Handle GET requests.
        """
        #data = {"message": "This is a GET request"}
        #return Response(data)
        return Response("Boilerlate correctamente configurado")