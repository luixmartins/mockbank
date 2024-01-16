from typing import Any
from django import forms 
from django.contrib.auth.models import User 
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError

from user.models import User as UserModel 

import re 

EMAIL_REGEX = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

class UserLoginForm(AuthenticationForm):
    def __init__(self,  *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['class'] = 'form-control'

class UserRegisterForm(forms.ModelForm):
    class Meta:
        model = UserModel 
        fields = ('user_phone', )
        labels = {
            'user_phone': 'Telefone', 
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