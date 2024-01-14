from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def loginUser(request):
    return render(request, 'login.html')