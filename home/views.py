from django.shortcuts import render, redirect

from home.forms import ContactForm
# Create your views here.
def home(request):
    if request.user.is_authenticated: 
        return redirect('user:home')
    
    return render(request, 'homepage.html')

def contact_us(request):

    if request.method == "POST":
        form = ContactForm(request.POST)

        if form.is_valid():
            name = request.POST['name']
            
            form.save()

            return render(request, 'contact_confirm.html', {'name': name})
        
        print(form.errors)
        return render(request, 'contact.html', {'form': form})
    
    form = ContactForm()

    context = {
        "form": form, 
    }

    return render(request, 'contact.html', context)