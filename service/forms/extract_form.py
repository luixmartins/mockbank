from django import forms 

class ExtractForm(forms.Form): 
    FILTER_CHOICES = [
        ('all', 'Todas'), 
        ('received', 'Recebidas'), 
        ('sent', 'Enviadas')
    ]
    
    filter_type = forms.ChoiceField(choices=FILTER_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

