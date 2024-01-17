from django.http import HttpResponse
from django.shortcuts import render, redirect 
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required


from user import forms 

def loginUser(request):
    if request.user.is_authenticated:
        redirect('userHome.html')

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

@login_required 
def home(request):
    return render(request, 'home.html', {'user': request.user})

@login_required
def profileUser(request): 
    ...