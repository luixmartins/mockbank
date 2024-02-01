from django import forms 

class ExtractForm(forms.Form): 
    FILTER_CHOICES = [
        ('all', 'Todas transações'), 
        ('received', 'Entrada'), 
        ('sent', 'Saída')
    ]
    
    filter_type = forms.ChoiceField(choices=FILTER_CHOICES, widget=forms.Select(attrs={'class': 'form-control form-control-lg mt-0 h-100'}))

