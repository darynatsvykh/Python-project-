
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import User 

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )

# class CustomUserCreationForm(forms.ModelForm):
#     class Meta:
#         model = User  # Explicitly reference the custom User model
#         fields = ['username', 'password']