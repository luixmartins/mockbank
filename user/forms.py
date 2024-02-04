from collections.abc import Mapping
from typing import Any
from django import forms 
from django.contrib.auth.models import User 
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList

from user.models import User as UserModel, UserMessages

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

class SentMessageForm(forms.ModelForm):
    user_to = forms.CharField(max_length=150, label='Enviar para', required=False,  widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'userInput'}))

    def __init__(self, *args, **kwargs): 
        from_user = kwargs.pop('from_user', None)

        super(SentMessageForm, self).__init__(*args, **kwargs)

        self.from_user = from_user 
        self.fields['user_to'].validators = []
    class Meta: 
        model = UserMessages
        fields = ('subject', 'message_content')

        labels = {
            'subject': 'Assunto', 
            'message_content': 'Mensagem', 
        }

        widgets = {
            'subject': forms.TextInput(attrs={
                'class': 'form-control', 
                'id': 'subjectInput', 
            }), 
            'message_content': forms.Textarea(attrs={
                'class': 'form-control', 
                'id': 'messageInput', 
            }), 
        }

    def clean_user_to(self): 
        username = self.cleaned_data['user_to']
        
        if username == '': 
            username = 'mockbank'

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise ValidationError('O contato informado não existe ou é inválido.')

        return user
    
    def save(self, commit=True): 
        instance = super().save(commit=False)
        instance.message_to = self.cleaned_data['user_to']
        instance.message_from = self.from_user 

        if commit: 
            instance.save()
        
        return instance 