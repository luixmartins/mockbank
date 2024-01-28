from django.shortcuts import render, redirect
from django.contrib import messages 
from django.views.generic.base import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from asgiref.sync import sync_to_async

from . import forms 
from .services import TransferService, SimulateLoanService
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

async def NotLoggedLoan(request): 
    if request.method == 'POST': 
        form = forms.LoanSimulateForm(request.POST)

        if form.is_valid(): 
            response = await SimulateLoanService.simulate_loan_api(request)

            if response['response'] == True: 
                messages.success(request, "Seu empréstimo pode ser aprovado!")
            elif response['response'] == False: 
                messages.success(request, "Seu empréstimo não pode ser aprovado no momento!")
            else: 
                messages.success(request, "Não foi possível realizar a operação no momento.")

            return redirect('user:home')
        
        context = {
            'form': form 
        }
        return render(request, 'not_logged_loan.html', context)
    
    context = {
        'form': forms.LoanSimulateForm()
    }

    return render(request, 'not_logged_loan.html', context)

