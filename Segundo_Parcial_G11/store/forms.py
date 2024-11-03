from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from captcha.fields import CaptchaField

class CustomUserCreationForm(UserCreationForm):
    captcha = CaptchaField()

    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2', 'name', 'phone_number', 'direccion', 'email']
        widgets = {
            'Nombre de usuario': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
