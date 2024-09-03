from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from .models import User

class SignupForm(UserCreationForm):
    phone_number = forms.CharField(max_length=15, required=True)
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(max_length=255, required=False)

    class Meta:
        model = User
        fields = ('phone_number', 'name', 'email', 'password1', 'password2')

class LoginForm(forms.Form):
    phone_number = forms.CharField(max_length=15, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean(self):
        phone_number = self.cleaned_data.get('phone_number')
        password = self.cleaned_data.get('password')
        if phone_number and password:
            user = authenticate(phone_number=phone_number, password=password)
            if user is None:
                raise forms.ValidationError("Invalid login credentials")
        return super().clean()
