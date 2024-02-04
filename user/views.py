from typing import Any

from django.shortcuts import render, redirect 
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User 
from django.views.generic.base import TemplateView, View
from django.views.generic import DetailView, ListView, CreateView
from django.urls import reverse 

from user import forms 
from user.models import User as BaseUser, UserMessages
from user.services import UserService

class LoginUser(View):
    def post(self, request): 
        form = forms.UserLoginForm(request, self.request.POST)

        if form.is_valid():
            user = form.get_user()
            auth.login(request, user)

            return redirect('user:home')
        
        context = {
            'form': form, 
        }   

        return render(request, 'login.html', context)         

    def get(self, request): 
        context = {
            'form': forms.UserLoginForm()
        }

        return render(request, 'login.html', context)

@method_decorator(login_required(login_url='user:login'), name='dispatch')
class LogoutUser(View):
    def get(self, request):
        auth.logout(request)

        return redirect('home:home')

class CreateUser(View):
    def get(self, request): 
        context = {
            'user_form': forms.UserRegisterForm(), 
            'member_form': forms.MemberRegisterForm(), 
        }

        return render(request, 'create.html', context)
    
    def post(self, request): 
        user_form = forms.UserRegisterForm(self.request.POST)
        member_form = forms.MemberRegisterForm(self.request.POST)

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
    
    

@method_decorator(login_required(login_url='user:login'), name='dispatch')
class HomePageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        context['user'] = UserService.get_user_django(username=self.request.user.username)
        context['account'] = UserService.user_balance(self.request.user.id)

        return context  
        
@method_decorator(login_required(login_url='user:login'), name='dispatch')
class ProfileUser(DetailView): 
    model = User
    template_name = 'profile_user.html'  
    context_object_name = 'user'  
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context =  super().get_context_data(**kwargs)

        context['base_user'] = UserService.get_user_app(self.object.id)

        return context 

@method_decorator(login_required(login_url='user:login'), name='dispatch')
class ListMessageUser(ListView): 
    model = UserMessages 
    template_name = 'list_messages.html'
    context_object_name = 'messages'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        context['messages'] = UserMessages.objects.filter(message_to = self.request.user)

        return context 
    
@method_decorator(login_required(login_url='user:login'), name='dispatch')
class MessageDetailView(DetailView): 
    model = UserMessages 
    template_name = 'detail_messages.html'
    context_object_name = 'message'
    slug_field = 'message_id'
    slug_url_kwarg = 'message_id'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        
        message = UserMessages.objects.get(message_id=self.kwargs['message_id'])

        if message.message_read is False: 
            message.message_read = True  
            
            message.save()

        context['message'] = message 

        return context 

@method_decorator(login_required(login_url='user:login'), name='dispatch')
class NewMessageView(View): 
    def get(self, request): 
        context = { 
            'form': forms.SentMessageForm()
        }

        return render(request, 'new_message_user.html', context)
    
    def post(self, request): 
        form = forms.SentMessageForm(request.POST, from_user=request.user)

        if form.is_valid(): 
            form.save()

            return redirect('user:list_messages')

        context = {
            'form': forms.SentMessageForm(request.POST, from_user=request.user)
        }

        return render(request, 'new_message_user.html', context)

            
    