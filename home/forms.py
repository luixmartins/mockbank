from collections.abc import Mapping
from typing import Any
from django import forms 
from django.core.exceptions import ValidationError

import re

from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList 

from home.models import ContactHome

EMAIL_REGEX = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

class ContactForm(forms.ModelForm):

    def __init__(self, *args, **kwargs) -> None:
        super(ContactForm, self).__init__(*args, **kwargs)

        self.fields['name'].label_suffix = ""
        self.fields['email'].label_suffix = ""
        self.fields['message'].label_suffix = ""

    class Meta:
        model = ContactHome 
        fields =  ("name", "email", "message")
        labels = {
            "name": "Nome", 
            "email": "Email", 
            "message": "Mensagem", 
        }
        
        widgets= {
            'name': forms.TextInput(attrs={
                'class': 'form-control', 
                'id': 'txtNome', 
                'placeholder': " ", 
            }), 
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'id': 'txtEmail', 
                'placeholder': " ", 
            }
            ), 
            'message': forms.Textarea(attrs={
                'class': 'form-control', 
                'id': 'txtmensagem', 
                'cols': "30", 
                'rows': '10', 
                'placeholder': ' ',
                'style':  "height:200px", 
            })

        }
    
    def clean_email(self):
        email = self.cleaned_data.get('email')

        if email and not re.match(EMAIL_REGEX, email):
            self.add_error(
                'name', 
                ValidationError(
                    'Email inválido', 
                    code='invalid', 
                ), 
            )
        
        return email 