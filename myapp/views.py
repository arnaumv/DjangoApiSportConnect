from rest_framework import viewsets
from .models import User
from .serializers import UserSerializer
from django.contrib.auth.hashers import check_password
from rest_framework import status, views
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse

from django.shortcuts import get_object_or_404
from rest_framework import permissions, views

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



## VIEW QUE COMPRUEBA EL ID DEL USERANME PARA CREAR EL EVENTO  (CREATE.HTML)

class UserIdView(views.APIView):
    def get(self, request, username, *args, **kwargs):
        try:
            user = User.objects.get(username=username)
            return JsonResponse({'id': user.id})
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

## VIEW CREAR EVENTO  (CREATE.HTML)
from rest_framework import viewsets
from .models import Event
from .serializers import EventSerializer

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


## VIEW PARA RESTABLECER CONTRASEÑA
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

@csrf_exempt
def reset_password(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')  # Get the email
            print(f"Resetting password for: {email}")  # Print the email

            # Create the email content
            message = Mail(
                from_email='gmail.com',
                to_emails=email,
                subject='Restablecer contraseña',
                html_content='Haz clic en el enlace para restablecer tu contraseña.'
            )

            try:
                # Send the email
                sg = SendGridAPIClient('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')
                response = sg.send(message)
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
