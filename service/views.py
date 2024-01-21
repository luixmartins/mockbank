from django.shortcuts import render, redirect
from django.contrib import messages 
from django.views.generic.base import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from . import forms 
from .services import TransferService
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