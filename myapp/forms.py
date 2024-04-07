# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.core.exceptions import ValidationError

class PasswordResetForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=200)

class PasswordResetConfirmForm(forms.Form):
    password1 = forms.CharField(label='Nueva contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar nueva contraseña', widget=forms.PasswordInput)

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 8 or len(password1) > 128:
            raise ValidationError("La contraseña debe tener entre 8 y 128 caracteres")
        return password1

    def clean_password2(self):
        password2 = self.cleaned_data.get('password2')
        if len(password2) < 8 or len(password2) > 128:
            raise ValidationError("La contraseña debe tener entre 8 y 128 caracteres")
        return password2

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")