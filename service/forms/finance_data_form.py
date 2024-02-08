from django import forms 

from user.models import FinanceDataUser, User 


class FinanceDataForm(forms.ModelForm): 
    class Meta: 
        model = FinanceDataUser 
        fields = ('dependents', 'education', 'employed', 'annual_income', 
                  'residential_assets', 'commercial_assets', 'luxury_assets', 
                  'bank_assets',)
        labels = {
            'dependents': 'Dependentes', 
            'education': 'Escolaridade', 
            'employed': 'Situação empregatícia',
            'annual_income': 'Renda anual (R$)', 
            'residential_assets': 'Patrimônio residencial', 
            'commercial_assets': 'Patrimônio comercial', 
            'luxury_assets': 'Patrimônio luxo', 
            'bank_assets': 'Patrimônio bancário',  
        }

    def __init__(self, *args, **kwargs): 
        user = kwargs.pop('user', None)

        super(FinanceDataForm, self).__init__(*args, **kwargs)

        self.user = User.objects.get(owner=user)
        
        self.fields['dependents'].widget.attrs.update({
            'class': 'form-control', 
        })
        self.fields['education'].widget.attrs.update({
            'class': 'form-control', 
        })
        self.fields['employed'].widget.attrs.update({
            'class': 'form-control', 
        })
        self.fields['annual_income'].widget.attrs.update({
            'class': 'form-control', 
        })
        self.fields['residential_assets'].widget.attrs.update({
            'class': 'form-control', 
        })
        self.fields['commercial_assets'].widget.attrs.update({
            'class': 'form-control', 
        })
        self.fields['luxury_assets'].widget.attrs.update({
            'class': 'form-control', 
        })
        self.fields['bank_assets'].widget.attrs.update({
            'class': 'form-control', 
        })

        self.label_suffix = ''
    
    def save(self, commit=True): 
        instance = super().save(commit=False)
        
        #instance.user = self.user 

        if commit: 
            instance.save()
        return instance 
