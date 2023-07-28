from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User

from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

def Activate(request, uidb64, token):
    try: 
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, 'E-Posta Onayınız İçin Teşekkür Ederiz.')
        return redirect('Login')
    else:
        messages.error(request, 'E-Posta Onayınız İçin Teşekkür Ederiz.')
        return redirect('home')

def ActiveEmail(request, user):
    current_site = get_current_site(request)
    mail_subject = "Hesabınızı Aktifleştirin"
    message = render_to_string('activate_account.html',{
        'user':user,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token':default_token_generator.make_token(user),
        'domain': current_site.domain,
    })
    send_mail(mail_subject, message, settings.EMAIL_HOST_USER, [user.email])

def home(request):
    return render(request,'home.html')


def Login(request):


    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
    
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'login.html')

def Register(request):
    if request.method == "POST":
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password1 = request.POST.get('password1')

        user = User.objects.create_user(first_name = name, last_name = surname, username=username, email=email, password=password)
        user.is_active = False
        user.save()
        ActiveEmail(request, user)
        return redirect('Login')
    return render(request, 'register.html')
