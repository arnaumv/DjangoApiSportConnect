from rest_framework import viewsets
from .models import User
from .serializers import UserSerializer
from django.contrib.auth.hashers import check_password
from rest_framework import status, views
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
        
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