from django.contrib.auth.hashers import check_password
from django.db import IntegrityError
from django.shortcuts import render
from rest_framework.authtoken.models import Token

from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Usuario
from .serializers import UsuarioSerializer

class UsuarioView(APIView):
    def post(self, request):
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=201)
            except IntegrityError:
                return Response({"error": "A user with this email already exists."}, status=400)
        return Response(serializer.errors, status=400)

class LoginView(APIView):
    def post(self, request):
        try:
            user = Usuario.objects.get(email=request.data.get('email'))
            if check_password(request.data.get('contrasena'), user.contrasena):
                return Response({"message": "Login successful"}, status=200)
            else:
                return Response({"error": "Invalid password"}, status=400)
        except Usuario.DoesNotExist:
            return Response({"error": "User does not exist"}, status=400)