from typing import Any
from django.shortcuts import render, redirect 
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User 
from django.views.generic.base import TemplateView


from user import forms 
from user.models import User as BaseUser 

def loginUser(request):
    if request.method == 'POST': 
        form = forms.UserLoginForm(request, request.POST)

        if form.is_valid():
            user = form.get_user()
            auth.login(request, user)

            return redirect('user:home')
        
        context = {
            'form': form, 
        }   

        return render(request, 'login.html', context)         

    context = {
        'form': forms.UserLoginForm()
    }

    return render(request, 'login.html', context)

@login_required
def logoutUser(request):
    auth.logout(request)

    return redirect('home:home')

def createUser(request):
    if request.method == 'POST':
        user_form = forms.UserRegisterForm(request.POST)
        member_form = forms.MemberRegisterForm(request.POST)

        if user_form.is_valid() and member_form.is_valid():
            member = member_form.save()
            user = user_form.save(commit=False)

            user.owner = member 
            user.save()

            messages.success(request, f"Sua conta foi criada Sr(a) { member.first_name }, ficamos felizes em ter você aqui!")

            return redirect('user:login')
        context = {
            'user_form': user_form, 
            'member_form': member_form, 
        }    

        return render(request, 'create.html', context)
    
    context = {
        'user_form': forms.UserRegisterForm(), 
        'member_form': forms.MemberRegisterForm(), 
    }

    return render(request, 'create.html', context)

@method_decorator(login_required(login_url='user:login'), name='dispatch')
class HomePageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        user_logged = User.objects.get(username=self.request.user.username) 
        account = BaseUser.objects.get(owner=user_logged.id)

        context['user'] = user_logged   

        data = {
            'balance': account.account_balance, 
            'limit': account.account_balance + account.account_limit, 
            'used_limit': account.account_limit - (account.account_balance + account.account_limit), 
        }

        context['account'] = data
    
        return context  
        
@login_required
def profileUser(request): 
    ...