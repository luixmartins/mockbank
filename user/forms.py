from django import forms 
from django.contrib.auth.models import User 
from django.core.exceptions import ValidationError

from user.models import User as UserModel 

import re 

EMAIL_REGEX = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control', 
            'placeholder': ' ', 
            'id': 'txtUser', 
            'required': True, 
        }
    ))

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control', 
            'placeholder': ' ', 
            'id': 'txtPassword', 
            'required': True, 
        }
    ))

class UserRegisterForm(forms.ModelForm):
    class Meta:
        model = UserModel 
        fields = ('phone')
        labels = {
            'phone': 'Telefone', 
        }

        widgets = {

        }
         

class UserAuthRegisterForm(forms.Form): 
    class Meta:
        model = User 
        fields = (
            'first_name', 'last_name', 'email', 
            'username', 'password1', 'password2', 
        )

        labels = {
            'first_name': "Nome", 
            'last_name': "Sobrenome", 
            'email': 'Email', 
            'username': "Usuário", 
            'password1': "Senha", 
            'password2': "Confirmação de senha", 
        }

        widgets = {
            
        }
        
    def clean_email(self):
        email = self.cleaned_data.get('email')

        if email and not re.match(EMAIL_REGEX, email):
            self.add_error(
                'txtEmail', 
                ValidationError(
                    'Email inválido', 
                    code='invalid', 
                ), 
            )
        
        return email 