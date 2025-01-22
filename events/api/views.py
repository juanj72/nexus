from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from events.api.serializers import EventSerializer,AttendanceSerializer
from events.models import Event, Attendance
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance


# clase que contiene los protocolos de la API de eventos
class EventList(APIView):
    @swagger_auto_schema(
        operation_description="Obtiene la lista de eventos",
        responses={200: "Lista de eventos"},
        
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
               'location': openapi.Schema(
                type=openapi.TYPE_OBJECT,
                description='Ubicación del evento en formato GeoJSON',
                properties={
                    'type': openapi.Schema(type=openapi.TYPE_STRING, description='Siempre "Point"', default='Point'),
                    'coordinates': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        description='Coordenadas [longitud, latitud]',
                        items=openapi.Schema(type=openapi.TYPE_NUMBER),
                        example=[-73.572229, 4.257138]
                    ),
                },
                required=['type', 'coordinates']
            ),
                'description': openapi.Schema(type=openapi.TYPE_STRING, description='Descripción del evento'),
                'event_manager': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID del administrador del evento'),
                'status': openapi.Schema(type=openapi.TYPE_STRING, description='Estado del evento, (active, inactive, cancelled, ended)'),
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
    
# clase que contiene los protocolos de la API de asistencias
class AttendanceList(APIView):


    def _convert_distance_to_meters(self, distance):
        return distance*111320

    def _validate_distance(self, request):
        event = Event.objects.get(id=request.data['event'])
        point_root = event.location
        point_attendance = request.data['location_attendance']

        if point_attendance['type'] == 'Point':
            location_attendante = Point(*point_attendance['coordinates'])
            distance = location_attendante.distance(point_root)

            distance_meters = self._convert_distance_to_meters(distance)

            if distance_meters > 50:
                return {"distance": distance_meters,"valid":False}
            else:
                return {"distance": distance_meters,"valid":True}
        else:
            return {"distance": 0,"valid":False}
    @swagger_auto_schema(
        operation_description="Obtiene la lista de asistencias",
        responses={200: "Lista de asistencias"},
        
        
    )
    def get(self, request):
        attendances = Attendance.objects.all()
        serializer = AttendanceSerializer(attendances, many=True)
        return Response(serializer.data)
    @swagger_auto_schema(
        operation_description="Crea una nueva asistencia",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'user': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID del usuario'),
                'event': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID del evento'),
                'date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, description='Fecha de la asistencia'),
                'entry_time': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, description='Hora de entrada'),
                'departure_time': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, description='Hora de salida'),
                'location_attendance': openapi.Schema(
                type=openapi.TYPE_OBJECT,
                description='Ubicación del evento en formato GeoJSON',
                properties={
                    'type': openapi.Schema(type=openapi.TYPE_STRING, description='Siempre "Point"', default='Point'),
                    'coordinates': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        description='Coordenadas [longitud, latitud]',
                        items=openapi.Schema(type=openapi.TYPE_NUMBER),
                        example=[-73.572229, 4.257138]
                    ),
                },
                required=['type', 'coordinates']
            ),
            },
            required=['user', 'event', 'date'],
        ),
        responses={201: "Asistencia creada con éxito"}
    )
    def post(self, request):
        serializer = AttendanceSerializer(data=request.data)
        Distance = self._validate_distance(request)

        if serializer.is_valid() :
            if Distance['valid'] == True:
                serializer.save()
            else:
                return Response({
                    "errors":serializer.errors,
                "message":f"no te encuentras dentro del rango permitido para registrar tu asistencia, distancia: {Distance['distance']} metros"}, 
                status=status.HTTP_400_BAD_REQUEST)
            return Response({"message": f"Asistencia creada con éxito, distancia: {Distance['distance']} metros", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)