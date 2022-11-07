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
    form = PasswordResetForm()
    return render(
        request=request,
        template_name='reset_password.html',
        context={'form':form}
    )
    
def passwordResetConfirm(request, uidb64, token):    
    return redirect('reset_password.html')

def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            associated_user = get_user_model().objects.filter(Q(email=user_email)).first()
            if associated_user:
                subject = "Password Reset request"
                message = render_to_string("template_reset_password.html", {
                    'user': associated_user,
                    'domain': get_current_site(request).domain,
                    'uid': urlsafe_base64_encode(force_bytes(associated_user.pk)),
                    'token': account_activation_token.make_token(associated_user),
                    "protocol": 'https' if request.is_secure() else 'http'
                })
                email = EmailMessage(subject, message, to=[associated_user.email])
                if email.send():
                    messages.success(request,
                        """
                        <h2>Password reset sent</h2><hr>
                        <p>
                            We've emailed you instructions for setting your password, if an account exists with the email you entered. 
                            You should receive them shortly.<br>If you don't receive an email, please make sure you've entered the address 
                            you registered with, and check your spam folder.
                        </p>
                        """
                    )
                else:
                    messages.error(request, "Problem sending reset password email, <b>SERVER PROBLEM</b>")

            return redirect('homepage')

        for key, error in list(form.errors.items()):
            if key == 'captcha' and error[0] == 'This field is required.':
                messages.error(request, "You must pass the reCAPTCHA test")
                continue

    form = PasswordResetForm()
    return render(
        request=request, 
        template_name="password_reset.html", 
        context={"form": form}
        )
            