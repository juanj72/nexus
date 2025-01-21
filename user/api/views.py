from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from user.api.serializers import UserSerializer
from user.models import User
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class UserView(APIView):
    @swagger_auto_schema(
        operation_description="Obtiene la lista de usuarios",
        responses={200: "Lista de usuarios"},
        tags=["User"]    

    )
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    