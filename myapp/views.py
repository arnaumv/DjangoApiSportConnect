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
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from .forms import PasswordResetForm, PasswordResetConfirmForm
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import smart_str



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
        return Response(serializer.data)  # Devolver los datos serializados directamente

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
        location = self.request.query_params.get('location', None)  # Obtén la ubicación de los parámetros de consulta
        if sport is not None:
            queryset = queryset.filter(sport__iexact=sport)  # Case-insensitive exact match
        if location is not None:
            queryset = queryset.filter(location__icontains=location)  # Case-insensitive contains match
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


## VIEW PARA COMPROBAR SI EL EMAIL EXISTE EN LA TABLA DE USUARIOS
@csrf_exempt
def check_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        User = get_user_model()
        exists = User.objects.filter(email__exact=email).exists()
        return JsonResponse({'exists': exists})
    else:
        return JsonResponse({'status': 'error', 'errors': 'Invalid request'}, status=400)



## VIEW PARA ENVIAR MENSAJE DE CORREO ELECTRONICO PARA RESTABLECER CONTRASEÑA
@csrf_exempt
def reset_password(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')  # Get the email
            print(f"Resetting password for: {email}")  # Print the email

            # Get the user
            User = get_user_model()
            try:
                user = User.objects.get(email__iexact=email)
            except User.DoesNotExist:
                print(f"No existe un usuario con el correo electrónico: {email}")
                return JsonResponse({'status': 'error', 'errors': 'No existe un usuario con este correo electrónico'}, status=400)

            # Generate the token
            token = default_token_generator.make_token(user)

            # Generate the uid
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            # Create the email content
            subject = 'Restablecer contraseña'
            #current_site = get_current_site(request)
            password_reset_url = f"https://sportconnect.ieti.site{reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})}"
            message = f'Haz clic en el enlace para restablecer tu contraseña: {password_reset_url}'
            from_email = 'sportconnect@gmail.com' 

            # Set is_reset_link_used to False
            user.is_reset_link_used = False
            user.save()

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

# VIEW PARA RESTABLECER LA CONTRASEÑA
@csrf_exempt
def password_reset_confirm(request, uidb64, token):
    message = ''
    if request.method == 'POST':
        form = PasswordResetConfirmForm(request.POST)
        if form.is_valid():
            try:
                # Decode the user id
                uid = smart_str(urlsafe_base64_decode(uidb64))

                # Get the user
                User = get_user_model()
                user = User.objects.get(pk=uid)

                # Check if the reset link has been used
                if user.is_reset_link_used:
                    message = 'El enlace de restablecimiento ya se ha utilizado'
                    form = PasswordResetConfirmForm()  # Reset the form

                # Check the token
                elif not default_token_generator.check_token(user, token):
                    message = 'Invalid token'
                    form = PasswordResetConfirmForm()  # Reset the form

                else:
                    # Get the new passwords
                    password1 = form.cleaned_data.get('password1')
                    password2 = form.cleaned_data.get('password2')

                    # Check that the two passwords match
                    if password1 != password2:
                        message = 'Las contraseñas no coinciden'
                        form = PasswordResetConfirmForm()  # Reset the form

                    else:
                        # Update the user's password
                        user.set_password(password1)
                        user.is_reset_link_used = True  # Mark the reset link as used
                        user.save()

                        # Set the success message
                        message = 'La contraseña se ha restablecido correctamente'

            except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                message = 'Invalid uid'
                form = PasswordResetConfirmForm()  # Reset the form

    else:
        form = PasswordResetConfirmForm()

    return render(request, 'myapp/password_reset_confirm.html', {'form': form, 'message': message})

# VIEW PARA ACTUALIZAR LOS DATOS DEL USUARIO
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import get_user_model
from django.conf import settings
import os

@api_view(['POST'])
def update_user(request, username):
    try:
        user = User.objects.get(username=username)
        
        # Verificar y actualizar los campos del usuario con los datos recibidos
        if 'email' in request.data and request.data['email'] != "":
            user.email = request.data['email']
        if 'password' in request.data and request.data['password'] != "":
            user.set_password(request.data['password'])
        if 'description' in request.data and request.data['description'] != "":
            user.description = request.data['description']
        if 'birthdate' in request.data and request.data['birthdate'] != "":
            user.birthdate = request.data['birthdate']
        if 'instagram' in request.data and request.data['instagram'] != "":
            user.instagram = request.data['instagram']  # Nuevo campo Instagram
        if 'twitter' in request.data and request.data['twitter'] != "":
            user.twitter = request.data['twitter']  # Nuevo campo Twitter

        # Manejar la subida de la imagen
        if 'image' in request.FILES:
            image = request.FILES['image']
            fs = FileSystemStorage()
            filename = fs.save(image.name, image)  # Eliminar 'profile_photos/' aquí
            user.image_path = filename  # Guardar solo la ruta relativa aquí

        user.save()
        return JsonResponse({'message': 'Los cambios se han restablecido correctamente', 'image_url': user.image_path.url})
    except User.DoesNotExist:
        return JsonResponse({'error': 'Usuario no encontrado'}, status=404)
    

# VIEW PARA MOSTRAR NOTIFICACIONES CUANDO SE UNE A UN EVENTO.  
from django.http import JsonResponse
from django.views import View
from .models import EventsJoined

class EventsJoinedView(View):
    def get(self, request, *args, **kwargs):
        username = request.GET.get('username')
        events = EventsJoined.objects.filter(user_id__username=username, notify_deleted=False).values('join_date', 'event__title', 'event__sport', 'event__location', 'event__date', 'event__time', 'event__id')  # Include event__id in the returned fields
        return JsonResponse(list(events), safe=False)


# VIEW PARRA CUANDO EL USUARIO ELIMINA UNA NOTIFICACION

import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import EventsJoined, Event
from django.core.exceptions import ObjectDoesNotExist

@csrf_exempt
def delete_notification(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        event_id = data.get('event_id')

        print('Username:', username)  # Print the username
        print('Event ID:', event_id)  # Print the event id

        try:
            # Try to find the event in the EventsJoined model
            event = EventsJoined.objects.get(user_id__username=username, event__id=event_id)
            event.notify_deleted = True
            event.save()
        except ObjectDoesNotExist:
            try:
                # If not found in EventsJoined, try to find it in the Event model
                event = Event.objects.get(user__username=username, id=event_id)
                event.deleted_notify = True
                event.save()
            except ObjectDoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Event not found'})

        return JsonResponse({'status': 'success'})
        
## VIEW PARA SELECCIOANR LOS EVENTOS CREADOS POR EL USUARIO Y MOSTRARLOS EN LAS NOTIFICACIONES
from django.http import JsonResponse
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from .models import Event, User

class EventsCreatedView(View):
    def get(self, request, *args, **kwargs):
        username = request.GET.get('username')
        print(f"Username received: {username}")  # Print the received username
        try:
            user = User.objects.get(username=username)
            print(f"User found: {user}")  # Print the found user

            # Filter out events that have deleted_notify set to True
            events = Event.objects.filter(user=user.id, deleted_notify=False).values('date', 'title', 'sport', 'location', 'date', 'time', 'id')
            print(f"Events found: {events}")  # Print the found events

            return JsonResponse(list(events), safe=False)
        except ObjectDoesNotExist:
            print("User not found")  # Print a message when the user is not found
            return JsonResponse({'error': 'Usuario no encontrado'}, status=404)
        

#ELEIMINAR UN EVENTO
@csrf_exempt
def delete_event(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        event_id = request.POST.get('event_id')

        try:
            # Buscar el evento
            event = Event.objects.get(id=event_id, user__username=username)
            event.delete()
            return JsonResponse({'message': 'Evento borrado correctamente'})
        except Event.DoesNotExist:
            return JsonResponse({'error': 'No se encontró el evento'}, status=404)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    




# @csrf_exempt
# def upload_image(request, username):
#     if request.method == 'POST':
#         image = request.FILES['image']
#         fs = FileSystemStorage()
#         filename = fs.save(image.name, image)
#         image_url = fs.url(filename)

#         # Concatenar MEDIA_ROOT con la URL de la imagen para obtener la ruta completa
#         image_path = os.path.join(settings.MEDIA_ROOT, image_url.lstrip('/'))

#         User = get_user_model()
#         try:
#             user = User.objects.get(username=username)
#             user.image_path = image_path
#             user.save()
#         except User.DoesNotExist:
#             return JsonResponse({'error': 'User does not exist'}, status=404)

#         return JsonResponse({'image_url': image_url})