from django.shortcuts import render, redirect
from django.contrib import messages 
from django.views.generic.base import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator

from . import forms 
from .services import TransferService, SimulateLoanService, ExtractService
from user.services import UserService

@method_decorator(login_required(login_url='user:login'), name='dispatch')
class TransferPage(View):
    def get(self, request):
        context = {
            'form': forms.TransferForm(from_user=request.user), 
            'account': UserService.user_balance(self.request.user.id), 
        }

        return render(request, 'transfer_page.html', context)

    def post(self, request):
        form = forms.TransferForm(request.POST, from_user=request.user)

        if form.is_valid(): 
            transfer_to = form.cleaned_data['received_by_username']
            
            data = {
                'sent_user': self.request.user.id, 
                'received_user': transfer_to.id, 
                'value': form.cleaned_data['value'], 
            }
            
            TransferService.update_account_balance(data)

            form.save()

            messages.success(request, f"Você realizou uma transferência para { transfer_to.username }.")
            
            return redirect('user:home')
        
        context = {
            'form': forms.TransferForm(request.POST, from_user=request.user), 
            'account': UserService.user_balance(self.request.user.id), 
        }
        return render(request, 'transfer_page.html', context)

@method_decorator(login_required(login_url='user:login'), name='dispatch')
class ExtractAccountView(View): 
    template_name = 'extract_page.html' 
    form_class = forms.ExtractForm
    
    def get(self, request, *args, **kwargs):
        form = self.form_class(request.GET)

        filter_type = form['filter_type'].value() if form.is_valid() else 'all' 

        queryset = ExtractService.extract_account(filter_type=filter_type, user_id=request.user.id)
        paginator = Paginator(queryset, 8)
        page_number = request.GET.get("page")

        page_obj = paginator.get_page(page_number)
        
        context = {
            'form': form, 
            'page_obj': page_obj, 
        }

        return render(request, self.template_name, context)
    
async def NotLoggedLoan(request): 
    if request.method == 'POST': 
        form = forms.LoanSimulateForm(request.POST)

        if form.is_valid(): 
            context = {
                'response': await SimulateLoanService.simulate_loan_api(request), 
                'name': request.POST.get('name'), 
            }

            return render(request, 'response_loan.html', context)
        
        context = {
            'form': form 
        }
        return render(request, 'not_logged_loan.html', context)
    
    context = {
        'form': forms.LoanSimulateForm()
    }

    return render(request, 'not_logged_loan.html', context)



