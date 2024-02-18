from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate

import datetime 

from service.models import TransferModel
from user.models import User 

class DepositForm(forms.ModelForm): 
    password = forms.CharField(required=True, label="Senha (A mesma utilizada para login)", label_suffix="", widget=forms.PasswordInput(attrs={
        'class': 'form-control', 
        'id': 'passwordInput', 
    }))

    class Meta: 
        model = TransferModel
        fields = ('value', )
        labels = {
            'value': 'Valor do depósito', 
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
 
        self.user = user 
        self.fields['value'].widget.attrs.update({
            'class': 'form-control', 
            'id': 'valueInput', 
            'min': '0', 
            'max': '999', 
        })

        self.fields['value'].label_suffix=""

    def clean_password(self): 
        password = self.cleaned_data['password']
 
        auth = authenticate(username=self.user.username, password=password)
        
        if auth: 
            return password

        raise ValidationError("Senha incorreta, tente novamente.") 
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        user = User.objects.get(owner=self.user)

        instance.sent_by = user
        instance.category = 'deposit'

        user.account_balance += self.cleaned_data['value']
        if user.finance_data.score < 1000: 
            user.finance_data.score += 10

        if commit:
            instance.save()
            user.finance_data.save()
            user.save()

        return instance

