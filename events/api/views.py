from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from events.api.serializers import EventSerializer
from events.models import Event, Attendance
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi



class EventList(APIView):
    @swagger_auto_schema(
        operation_description="Obtiene la lista de eventos",
        responses={200: "Lista de eventos"}
    )
    def get(self, request):
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Crea un nuevo evento",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre del evento'),
                'date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, description='Fecha del evento'),
            },
            required=['name', 'date'],
        ),
        responses={201: "Evento creado con éxito"}
    )
    def post(self, request):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)