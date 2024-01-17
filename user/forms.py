from typing import Any
from django import forms 
from django.contrib.auth.models import User 
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError

from user.models import User as UserModel 

class UserLoginForm(AuthenticationForm):
    def __init__(self,  *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['class'] = 'form-control'

class UserRegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self,).__init__(*args, **kwargs)

        self.label_suffix = ''
    class Meta:
        model = UserModel 
        fields = ('user_phone', )
        labels = {
            'user_phone': 'Telefone de contato', 
        }

        widgets = {
            'user_phone': forms.TextInput(attrs={
                'class': 'form-control', 
            }),
        }

class MemberRegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(MemberRegisterForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'

        self.label_suffix = ''

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 
                  'email', 'password1', 'password2', )
        
        labels = {
            'username': 'Usuário', 
            'first_name': 'Nome', 
            'last_name': 'Sobrenome', 
            'email': 'Endereço de Email', 
            'password1': 'Senha', 
            'password2': 'Confirmação de senha', 
        }

        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control', 
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control', 
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control', 
            }), 
        }