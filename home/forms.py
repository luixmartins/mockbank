from django import forms 
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator

import re 

from home.models import ContactHome

EMAIL_REGEX = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

class ContactForm(forms.ModelForm):
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
                'autofocus': True, 
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