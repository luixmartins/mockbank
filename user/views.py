from django.shortcuts import render, redirect 
from django.contrib import auth 
from django.contrib.auth.decorators import login_required

from user.forms import * 

def loginUser(request):
    if request.user.is_authenticated:
        redirect('userHome.html')

    if request.method == 'POST': 
        form = UserLoginForm(request, request.POST)

        if form.is_valid():
            user = form.get_user()
            auth.login(request, user)

            return redirect('user:home')
        
        context = {
            'form': form, 
        }   

        return render(request, 'login.html', context)         

    context = {
        'form': UserLoginForm()
    }

    return render(request, 'login.html', context)

@login_required 
def home(request):
    return render(request, 'home.html', {'user': request.user})