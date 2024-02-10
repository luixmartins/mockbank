from django import forms 

from user.models import FinanceDataUser, User 


class FinanceDataForm(forms.ModelForm): 
    EDUCATION_CHOICE = [
        ("1", "Graduação completa"), 
        ("0", "Graduação incompleta"), 
    ]

    EMPLOYED_CHOICE = [
        ("1", "Empregado"), 
        ("0", "Não empregado"), 
    ]

    education = forms.ChoiceField(choices=EDUCATION_CHOICE, label="Educação", required=True, widget=forms.Select(attrs={"class": "form-select", "id": "educacaoInput"}))
    employed = forms.ChoiceField(choices=EMPLOYED_CHOICE, label="Situação empregatícia", required=True, widget=forms.Select(attrs={"class": "form-select", "id": "empregoInput"}))

    class Meta: 
        model = FinanceDataUser 
        fields = ('dependents',  'annual_income', 
                  'residential_assets', 'commercial_assets', 'luxury_assets', 
                  'bank_assets',)
        labels = {
            'dependents': 'Dependentes', 
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
            'id': 'dependentesInput', 
        })
        self.fields['education'].widget.attrs.update({
            'class': 'form-control', 
            'id': 'educacaoInput', 
        })
        self.fields['employed'].widget.attrs.update({
            'class': 'form-control', 
            'id': 'empregoInput', 
        })
        self.fields['annual_income'].widget.attrs.update({
            'class': 'form-control',
            'id': 'rendaInput' 
        })
        self.fields['residential_assets'].widget.attrs.update({
            'class': 'form-control',
            'id': 'residencialInput',  
        })
        self.fields['commercial_assets'].widget.attrs.update({
            'class': 'form-control', 
            'id': 'comercialInput', 
        })
        self.fields['luxury_assets'].widget.attrs.update({
            'class': 'form-control',
            'id': 'luxoInput',  
        })
        self.fields['bank_assets'].widget.attrs.update({
            'class': 'form-control',
            'id': 'bancoInput' 
        })

        self.label_suffix = ''
    
    def save(self, commit=True): 
        instance = super().save(commit=False)
        
        instance.user = self.user 
        instance.employed = int(self.cleaned_data['employed'])
        instance.education = int(self.cleaned_data['education'])

        if commit: 
            instance.save()
        return instance 
