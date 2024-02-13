from typing import Any, Mapping
from django import forms 
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.forms.renderers import BaseRenderer
from django.forms.utils import ErrorList

class LoanForm(forms.Form): 
    value = forms.DecimalField(decimal_places=2, min_value=0, required=True, label='Valor (R$)', label_suffix='')
    payment = forms.DecimalField(decimal_places=0, min_value=8, max_value=72, required=True, label='Pagamento (meses)', label_suffix='')

    def __init__(self, *args, **kwargs): 
        super(LoanForm, self).__init__(*args, **kwargs)

        self.fields['value'].widget.attrs.update({
            'class': 'form-control', 
            'id': 'ValorInput', 
        })
        self.fields['payment'].widget.attrs.update({
            'class': 'form-control', 
            'id': 'PagamentoInput', 
        })

class ConfirmLoanForm(forms.Form): 
    password = forms.CharField(required=True, label="Senha (A mesma utilizada para login)", label_suffix="", widget=forms.PasswordInput(
        attrs={
            'class': 'form-control', 
            'id': 'passwordInput', 
        }
    ))

    def __init__(self, *args, **kwargs) -> None:
        user = kwargs.pop('user', None)
        
        super(ConfirmLoanForm, self).__init__(*args, **kwargs)

        self.user = user 

    def clean_password(self): 
        password = self.cleaned_data['password']
 
        auth = authenticate(username=self.user.username, password=password)
        
        if auth: 
            return password

        raise ValidationError("Senha incorreta, tente novamente.") 

