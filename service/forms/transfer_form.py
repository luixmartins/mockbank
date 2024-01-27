from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from user.models import User as BaseUser
from service.models import TransferModel

class TransferForm(forms.ModelForm):
    received_by_username = forms.CharField(max_length=150, label='Nome de Usuário', widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'txtUser'}))
    password = forms.CharField(label='Senha', widget=forms.PasswordInput(attrs={
        'class': 'form-control', 
        'id': 'txtPassword', 
    }))

    def __init__(self, *args, **kwargs):
        from_user = kwargs.pop('from_user', None)
        
        super(TransferForm, self).__init__(*args, **kwargs)

        self.from_user = from_user 
        self.fields['value'].widget.attrs.update({
                'class': 'form-control', 
                'id': 'txtValue', 
                'min': '0.01', 
                'value': '0.01', 
            })

    class Meta:
        model = TransferModel
        fields = ('value', 'received_by_username')
        labels = {
            'value': 'Valor da transferência', 
            'received_by_username': 'Enviar para', 
        }

    def clean_value(self):
        value = self.cleaned_data['value']
        base_user = BaseUser.objects.get(owner=self.from_user.id)
        
        if value > (base_user.account_balance + base_user.account_limit):
            raise ValidationError('Você não possui saldo suficiente para realizar esta transação.') 

        return value   

    def clean_received_by_username(self): 
        username = self.cleaned_data['received_by_username']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise ValidationError('O contato informado não existe ou é inválido.')

        if user == self.from_user: 
            raise ValidationError('Insira um contato válido.')

        return user
    
    def clean_password(self): 
        password = self.cleaned_data['password']
 
        auth = authenticate(username=self.from_user.username, password=password)
        
        if auth: 
            return password

        raise ValidationError("Senha incorreta, tente novamente.") 
        

    def save(self, commit=True):
        transfer_instance = super().save(commit=False)
        transfer_instance.received_by = self.cleaned_data['received_by_username']
        transfer_instance.sent_by = self.from_user

        if commit:
            transfer_instance.save()

        return transfer_instance
