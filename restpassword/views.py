from django.shortcuts import render
from . models import *
from django.http import HttpResponse, Http404 
from django.shortcuts import redirect
from .forms import PasswordResetForm

# Create your views here.
def register(request):
    if request.method == 'POST':
        Email=request.POST['Email']
        password=request.POST['Password']
        
        log=employee( Email=Email, password=password)
        
        log.save()
    
    return render(request, 'register.html')

def login(request):
    if request.method =='POST':
        email = request.post('email')
        password = request.post('password')
        emp=employee.object.filter(email=email, password=password)
        print(email)
        print(password)
        
        if emp.exists():
            return HttpResponse("login successfull")
        else:
            return HttpResponse("404 error")
        
    return render(request, 'login.html')

def reset_password(request):
    form = PasswordResetForm()
    return render(
        request=request,
        template_name='reset_password.html',
        context={'form':form}
    )
    
def passwordResetConfirm(request, uidb64, token):    
    return redirect('reset_password.html')

