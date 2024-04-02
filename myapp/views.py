from rest_framework import viewsets
from .models import User, Event, EventsJoined
from .serializers import UserSerializer, EventSerializer, EventsJoined, EventsJoinedSerializer
from django.contrib.auth.hashers import check_password
from rest_framework import status, views
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework import permissions, views
from rest_framework.decorators import api_view

# VIEW PARA CREAR USUARIO
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# VIEW PARA INICIAR SESION
class LoginView(views.APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        try:
            user = User.objects.get(username=username)
            if check_password(password, user.password):
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
            else:
                return Response({"error": "Invalid login credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return Response({"error": "Invalid login credentials"}, status=status.HTTP_401_UNAUTHORIZED)

# VIEW PARA DEVOLVER INFORMACION DEL USAURIO (PROFILE.HTML)
class UserProfileView(views.APIView):
    def get(self, request, username, *args, **kwargs):
        user = get_object_or_404(User, username=username)
        serializer = UserSerializer(user)
        return Response(serializer.data)

## VIEW QUE COMPRUEBA EL ID DEL USERANME PARA CREAR EL EVENTO (CREATE.HTML)
class UserIdView(views.APIView):
    def get(self, request, username, *args, **kwargs):
        try:
            user = User.objects.get(username=username)
            return JsonResponse({'id': user.id})
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)


## VIEW CREAR EVENTO (CREATE.HTML)
class EventCreateViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


## VIEW PARA MOSTRAR EVENTOS (EVENTS.HTML)
class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer

    def get_queryset(self):
        queryset = Event.objects.all()
        sport = self.request.query_params.get('sport', None)
        if sport is not None:
            queryset = queryset.filter(sport=sport)
        return queryset

    @action(detail=True, methods=['get'])
    def get_event(self, request, pk=None):
        try:
            event = Event.objects.get(pk=pk)
            serializer = EventSerializer(event)
            return Response(serializer.data)
        except Event.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'])
    def user_subscribed_events(self, request):
        username = request.query_params.get('username')
        if username:
            user = get_object_or_404(User, username=username)
            try:
                user_events = EventsJoined.objects.filter(user_id=user.id)
                event_ids = user_events.values_list('event_id', flat=True)
                subscribed_events = Event.objects.filter(id__in=event_ids)
                serializer = self.get_serializer(subscribed_events, many=True)
                return Response(serializer.data)
            except:
                return Response({"detail": "Error occurred while retrieving subscribed events."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"detail": "Username parameter is missing."}, status=status.HTTP_400_BAD_REQUEST)



## VIEW PARA UNIRSE A EVENTOS (INFOEVENT.HTML)
@api_view(['POST'])
def join_event(request):
    username = request.data.get('username')
    event_id = request.data.get('event')

    try:
        user = User.objects.get(username=username)
        event = Event.objects.get(pk=event_id)
    except (User.DoesNotExist, Event.DoesNotExist):
        return Response(status=status.HTTP_404_NOT_FOUND)

    events_joined = EventsJoined(user_id=user, username=username, event=event)
    events_joined.save()

    serializer = EventsJoinedSerializer(events_joined)
    return Response(serializer.data, status=status.HTTP_201_CREATED)



## VIEW PARA SALIR DE EVENTOS (INFOEVENT.HTML)
@api_view(['POST'])
def leave_event(request):
    username = request.data.get('username')
    event_id = request.data.get('event')

    try:
        # Obtener la instancia de User
        user = User.objects.get(username=username)
        print('User found:', user.username, user.id)  # Mensaje para la consola del servidor
    except User.DoesNotExist:
        print('User not found with username:', username)  # Mensaje para la consola del servidor
        return Response({"message": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    try:
        # Obtener la instancia de Event
        event = Event.objects.get(pk=event_id)
        print('Event found:', event.title, event.id)  # Mensaje para la consola del servidor
    except Event.DoesNotExist:
        print('Event not found with ID:', event_id)  # Mensaje para la consola del servidor
        return Response({"message": "Evento no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    try:
        # Verificar si el usuario está unido al evento
        event_joined = EventsJoined.objects.get(user_id_id=user.id, event_id=event.id)
        print('EventsJoined found:', event_joined.id)  # Mensaje para la consola del servidor
        # Eliminar la instancia de EventsJoined
        event_joined.delete()
        return Response({"message": "Usuario eliminado del evento correctamente"}, status=status.HTTP_204_NO_CONTENT)
    except EventsJoined.DoesNotExist:
        print('EventsJoined not found for user:', user.username, 'and event:', event.title)  # Mensaje para la consola del servidor
        return Response({"message": "El usuario no está unido a este evento"}, status=status.HTTP_404_NOT_FOUND)
    


## VIEW PARA COMPROVAR SI EL USUARIO YA ESTA UNIDO AL EVENTO
@api_view(['POST'])
def check_joined(request):
    username = request.data.get('username')
    event_id = request.data.get('event')

    try:
        user_joined = EventsJoined.objects.filter(username=username, event_id=event_id).exists()
    except EventsJoined.DoesNotExist:
        user_joined = False

    return Response({'joined': user_joined})




## VIEW PARA SALIR DE LA MLISTA DE PARTICIPANTES DE UN EVENTO
@api_view(['POST'])
def cancel_event(request):
    username = request.data.get('username')
    event_id = request.data.get('event')

    try:
        user = User.objects.get(username=username)
        event = Event.objects.get(pk=event_id)
    except (User.DoesNotExist, Event.DoesNotExist):
        return Response(status=status.HTTP_404_NOT_FOUND)

    try:
        event_joined = EventsJoined.objects.get(user_id=user.id, event_id=event.id)
        event_joined.delete()
        return Response({"message": "Usuario eliminado del evento correctamente"}, status=status.HTTP_204_NO_CONTENT)
    except EventsJoined.DoesNotExist:
        return Response({"message": "El usuario no está unido a este evento"}, status=status.HTTP_404_NOT_FOUND)


## VIEW PARA MOSTRAR PARTICIPANTES DE UN EVENTO (INFOEVENT.HTML)
@api_view(['GET'])
def get_participants(request, event_id):
    try:
        participants = EventsJoined.objects.filter(event_id=event_id)
        serializer = EventsJoinedSerializer(participants, many=True)
        return Response(serializer.data)
    except EventsJoined.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)





## VIEW PARA RESTABLECER CONTRASEÑA
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.core.mail import send_mail
from django.http import JsonResponse
from django.contrib.auth.forms import PasswordResetForm

@csrf_exempt

def reset_password(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')  # Get the email
            print(f"Resetting password for: {email}")  # Print the email

            # Create the email content
            subject = 'Restablecer contraseña'
            message = 'Haz clic en el enlace para restablecer tu contraseña.'
            from_email = 'amestrevizcaino.cf@iesesteveterrads.cat'  # Replace with your Gmail address

            try:
                # Send the email
                send_mail(subject, message, from_email, [email])
                print("Password reset email sent.")
                return JsonResponse({'status': 'success'})
            except Exception as e:
                print(f"Error sending email: {e}")
                return JsonResponse({'status': 'error', 'errors': str(e)}, status=400)
        else:
            print(f"Form errors: {form.errors}")
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    else:
        print("Invalid request.")
        return JsonResponse({'status': 'error', 'errors': 'Invalid request'}, status=400)
from django.contrib.auth.views import PasswordResetConfirmView

class PasswordResetConfirm(PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'
