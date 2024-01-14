from django.shortcuts import render, redirect 
from django.contrib.auth import authenticate
from django.contrib import auth 

from user.forms import * 

def loginUser(request):
    if request.user.is_authenticated:
        redirect('userHome.html')

    if request.method == 'POST': 
        form = UserLoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)

            if user is not None: 
                auth.login(request, user)

                return redirect('user:home')

            context = {
                'form': form, 
                'error': 'Credenciais inválidas, tente novamente.', 
            }
            
            return render(request, 'login.html', context)         

    context = {
        'form': UserLoginForm()
    }

    return render(request, 'login.html', context)

def home(request):
    return render(request, 'home.html')