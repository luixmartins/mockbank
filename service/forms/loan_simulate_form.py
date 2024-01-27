from collections.abc import Mapping
from typing import Any
from django import forms
from django.forms.utils import ErrorList 

class LoanSimulateForm(forms.Form):
    EDUCATION_CHOICE = [
        ("1", "Graduação completa"), 
        ("0", "Graduação incompleta"), 
    ]

    EMPLOYED_CHOICE = [
        ("1", "Empregado"), 
        ("0", "Não empregado"), 
    ]

    name = forms.CharField(max_length=50, required=True)
    
    education = forms.ChoiceField(choices=EDUCATION_CHOICE, label="Educação", required=True, widget=forms.Select(attrs={"class": "form-select", "id": "educacaoInput"}))
    employed = forms.ChoiceField(choices=EMPLOYED_CHOICE, label="Situação empregatícia", required=True, widget=forms.Select(attrs={"class": "form-select", "id": "empregoInput"}))
    
    dependents = forms.DecimalField(decimal_places=0, min_value=0, max_value=10, required=True)
    
    score = forms.DecimalField(decimal_places=1, min_value=0, max_value=1000, required=True)
    value = forms.DecimalField(decimal_places=2, min_value=0, required=True)
    payment = forms.DecimalField(decimal_places=0, min_value=8, max_value=72, required=True)
    
    annual_income = forms.DecimalField(decimal_places=2, min_value=0, required=True)
    residential_assets = forms.DecimalField(decimal_places=2, min_value=0, required=True)
    commercial_assets = forms.DecimalField(decimal_places=2, min_value=0, required=True)
    luxury_assets = forms.DecimalField(decimal_places=2, min_value=0, required=True)
    bank_assets = forms.DecimalField(decimal_places=2, min_value=0, required=True)

    def __init__(self, *args, **kwargs) -> None:
        super(LoanSimulateForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs.update({
            'class': 'form-control', 
            'id': 'nomeInput', 
        })
        self.fields['dependents'].widget.attrs.update({
            'class': 'form-control', 
            'id': 'dependentesInput', 
        })
        self.fields['score'].widget.attrs.update({
            'class': 'form-control', 
            'id': 'scoreInput', 
        })
        self.fields['value'].widget.attrs.update({
            'class': 'form-control monetary-mask', 
            'id': 'valorInput', 
        })
        self.fields['payment'].widget.attrs.update({
            'class': 'form-control', 
            'id': 'mesesInput', 
        })
        self.fields['annual_income'].widget.attrs.update({
            'class': 'form-control monetary-mask', 
            'id': 'rendaInput', 
        })
        self.fields['residential_assets'].widget.attrs.update({
            'class': 'form-control monetary-mask', 
            'id': 'residencialInput', 
        })
        self.fields['commercial_assets'].widget.attrs.update({
            'class': 'form-control monetary-mask', 
            'id': 'comercialInput', 
        })
        self.fields['luxury_assets'].widget.attrs.update({
            'class': 'form-control monetary-mask', 
            'id': 'luxoInput', 
        })
        self.fields['bank_assets'].widget.attrs.update({
            'class': 'form-control monetary-mask', 
            'id': 'bancarioInput', 
        })