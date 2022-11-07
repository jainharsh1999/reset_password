from django.shortcuts import render
from . models import *
from django.http import HttpResponse, Http404 
from django.shortcuts import redirect
from .forms import PasswordResetForm
from .forms import PasswordResetForm
from django.db.models.query_utils import Q
from django.conf import settings
from django.core.mail import send_mail
from django .contrib import messages
from .helper import send_forget_password_mail
import uuid


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
        email = request.POST['email']
        password = request.POST['password']
        emp=employee.objects.filter(Email=email, password=password)
        print(email)
        print(password)
        
        if emp.exists():
            return HttpResponse("login successfull")
        else:
            return HttpResponse("404 error")
        
    return render(request, 'login.html')

def reset_password(request):
    if request.method == "POST":
        email=request.POST['email']

        if not employee.objects.filter(email=email):
            messages.success(request,'No user found!')
            return redirect('forgetpassword')
        else:
            user_obj=employee.objects.get(email=email)
            token=str(uuid.uuid4())
            send_forget_password_mail(user_obj,token)
            messages.success(request,'An email is sent')    
            return redirect('forgetpassword')
    return render(request,"reset_password.html")
    
def passwordResetConfirm(request, uidb64, token):    
    return redirect('reset_password.html')

def reset_password(request):
    return render(request, 'reset_password.html')
            