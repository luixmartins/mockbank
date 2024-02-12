from django import forms 

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

