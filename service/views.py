from django.shortcuts import render, redirect
from django.contrib import messages 
from django.views.generic.base import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator, classonlymethod
from django.core.paginator import Paginator

from asgiref.sync import sync_to_async
import asyncio 

from . import forms 
from service.services import TransferService, SimulateLoanService, ExtractService, GetFinanceDataService, CreateNewLoanService
from user.services import UserService
from user.models import User 
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

            return render(request, 'response_not_logged_loan.html', context)
        
        context = {
            'form': form 
        }
        return render(request, 'not_logged_loan.html', context)
    
    context = {
        'form': forms.LoanSimulateForm()
    }

    return render(request, 'not_logged_loan.html', context)
@method_decorator(login_required(login_url='user:login'), name='dispatch')
class FinanceDataUserView(View): 
    def get(self, request): 
        user = User.objects.get(owner=request.user)

        if user.finance_data.active is False: 
            context = {
                'form': forms.FinanceDataForm(user=request.user, instance=user.finance_data),
                'subtitle': 'Primeiro, vamos registrar alguns de seus dados financeiros.', 
                'button': 'Enviar'
            }
            return render(request, 'finance_data_register.html', context)
        
        return redirect('service:loan')

    def post(self, request): 
        user = User.objects.get(owner=request.user)
        form = forms.FinanceDataForm(request.POST, user=request.user, instance=user.finance_data) 

        if form.is_valid(): 
            form = form.save(commit=False)
            
            form.active = True 
            form.save()
            messages.success(request, 'Suas informações foram registradas com sucesso!')

            return redirect('service:loan')
        context = { 
            'form': form,
            'subtitle': 'Primeiro, vamos registrar alguns de seus dados financeiros.', 
            'button': 'Enviar' 
        }

        return render(request, 'finance_data_register.html', context)
    
@method_decorator(login_required(login_url='user:login'), name='dispatch')
class FinanceDataUserUpdateView(View): 
    def get(self, request): 
        user = User.objects.get(owner=request.user)

        context = {
            'form': forms.FinanceDataForm(user=request.user, instance=user.finance_data),
            'subtitle': 'Atualizar dados', 
            'button': 'Salvar'
        }
        return render(request, 'finance_data_register.html', context)

    def post(self, request): 
        user = User.objects.get(owner=request.user)
        form = forms.FinanceDataForm(request.POST, user=request.user, instance=user.finance_data) 

        if form.is_valid(): 
            form.save()
            messages.success(request, 'Suas informações foram atualizadas com sucesso!')

            return redirect('user:home')
        context = { 
            'form': form,
            'subtitle': 'Atualizar dados', 
            'button': 'Salvar'
        }

        return render(request, 'finance_data_register.html', context)
    
@method_decorator(login_required(login_url='user:login'), name='dispatch')
class LoanView(View): 
    def get(self, request): 
        context = {
            'form': forms.LoanForm()
        }

        return render(request, 'loan.html', context)


@sync_to_async
def get_user_from_request(request) -> User | None:
    return request.user if bool(request.user) else None

@sync_to_async
def get_data(*args, **kwargs) -> dict | None: 
    data = GetFinanceDataService.get_finance_data(user=kwargs.get('user'), value=kwargs.get('value'), payment=kwargs.get('payment'))
    
    return data if data else None 


async def loan(request):
    user = await get_user_from_request(request) 
    if user: 
        form = forms.LoanForm(request.POST)

        if form.is_valid(): 
            data = await get_data(user=user, value=request.POST.get('value'), payment=request.POST.get('payment'))

            response = await SimulateLoanService.simulate_loan_api(data=data)
            
            if response is True: 
                request.session['data'] = {
                    'value': request.POST.get('value'), 
                    'payment': request.POST.get('payment'), 
                }

                return redirect('service:confirm_loan')

            else: 
                messages.error(request, "Infelizmente não podemos aprovar o valor solicitado neste momento.")

                return render(request, 'loan.html', {'form': form})            
        
        return render(request, 'loan.html', {'form': form})
    
    return redirect('user:login')

@method_decorator(login_required(login_url='user:login'), name='dispatch')
class ConfirmLoanView(View): 
    def get(self, request): 
        form = forms.ConfirmLoanForm(user=request.user)

        context = {
            'value': request.session['data'].get('value'), 
            'payment': request.session['data'].get('payment'), 
            'form': form, 
        }

        return render(request, 'confirm_loan.html', context)
    
    def post(self, request): 
        form = forms.ConfirmLoanForm(request.POST, user=request.user)

        if form.is_valid(): 
            value = request.session['data'].get('value')
            payment = request.session['data'].get('payment')

            response = CreateNewLoanService.create_loan(user=request.user, value=value, payment=payment)

            if response is not False: 
                messages.success(request, "Seu empréstimo foi realizado com sucesso! Em breve, o valor será debitado na sua conta.")

                del request.session['data']

                return redirect('user:home')
            
            messages.error(request, "A operação pode ser realizada apenas uma vez por dia.")
            
            return redirect('service:loan')
        
        context = {
            'value': request.session['data'].get('value'), 
            'payment': request.session['data'].get('payment'), 
            'form': form, 
        }

        return render(request, 'confirm_loan.html', context)

