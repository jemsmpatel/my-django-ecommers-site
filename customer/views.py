from django.shortcuts import render ,HttpResponse ,redirect
from django.contrib import messages
from .forms import Registration ,Login, Forgot_pass, OTP
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from seller.signals import email_sender
from django.db import IntegrityError
import random
import time
from home.models import User
import re

# Create your views here.
def loginuser(request):
    form = Login()
    if request.method == 'POST':
        form = Login(request.POST)
        if form.is_valid():
            user = authenticate(request, email=form.cleaned_data['email'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'you are loged in successfully.')
                return redirect('/')  # Redirect to the home page or dashboard
            else:
                messages.error(request, 'Invalid email or password')
                return redirect('/customer/login/')
    return render(request, 'login.html', {'form': form})

def logoutuser(request):
    logout(request)
    return redirect("/customer/login")

def registration(request):
    form = Registration()
    if request.method == 'POST':
        form = Registration(request.POST)
        print("rajisterd1")
        if form.is_valid():
            if form.cleaned_data['password'] == form.cleaned_data['password2']:
                if validate_password(form.cleaned_data['password']):
                    try:
                        get_user_model().objects.create_user(
                        email = form.cleaned_data['email'],
                        password = form.cleaned_data['password'],
                        full_name = form.cleaned_data['fname'],
                        contact_no = form.cleaned_data['contact']
                        )
                        messages.success(request, 'acoount is created.')
                        return redirect('/customer/login/')
                    except IntegrityError :
                        messages.error(request, 'you are alrady rajisterd in this site.')
                        return redirect('/customer/login/')
                else:
                    print("invalid")
            else:
                print("confirm password not match")
        else:
            print("error", form.errors)
    return render(request, 'registration.html',{'form': form})

def validate_password(password):
    # Check for lowercase, uppercase, digits, and special characters
    if (any(char.islower() for char in password) and
        any(char.isupper() for char in password) and
        any(char.isdigit() for char in password) and
        re.search(r'[!@#$%^&*(),.?":{}|<>]', password)):
        return True
    return False

def forgot_pass(request):
    if request.method == 'POST':
        form = Forgot_pass(request.POST)
        if form.is_valid():
            email1 = form.cleaned_data['email']
            try:
                User.objects.get(email = email1)
                print('user get')
                otp1 = random.randint(100000,999999)
                request.session['otp1'] = otp1
                request.session['user_email'] = email1
                try:
                    email_sender(email1, "otp", f"hiiii your otp is {otp1}")
                    messages.success(request, f'otp is sent on {email1} mail.')
                    print('mail sented')
                    return redirect('/customer/c_otp/')
                except Exception as e:
                    print(f"error {e}")
            except User.DoesNotExist:
                messages.error(request, 'user is not exist please sign up on this site.')
                return redirect('/customer/registration/')
    else:
        form = Forgot_pass()
        context = {
            'form': form,
            'pagetitle': 'Sign In',
            'formtitle': 'Forgot Password',
            'faction': '/customer/forgot_pass/',
            'infolink': '/customer/login/',
        }
    return render(request, 'forgot_pass.html', context)


def c_otp(request):
    if request.method == 'POST':
        form = OTP(request.POST)
        if form.is_valid():
            otp1 = request.session['otp1']
            email1 = request.session['user_email']
            otp = form.cleaned_data['otp']
            print(f"{otp},{otp1}")
            if form.cleaned_data['password'] == form.cleaned_data['password2']:
                if str(otp1) == str(otp):
                    user = User.objects.get(email = email1)
                    user.set_password(form.cleaned_data['password'])
                    user.save()
                    messages.success(request, 'password has been changed succssesfully.')
                    return redirect('/customer/login/')
                else:
                    messages.error(request, 'otp is not match.please try again')
                    return redirect('/customer/forgot_pass/')
            else:
                messages.error(request, 'confirm password is not match please try again.')
                return
    else:
        form = OTP()
        context = {
            'form': form,
            'pagetitle': 'Sign In',
            'formtitle': 'Sign In',
            'faction': '/customer/c_otp/',
            'infolink': '/customer/login/',
        }
    return render(request, 'forgot_pass.html', context)









def profile(request):
    if request.user.is_anonymous:
        return redirect("/customer/login/")
    try:
        user = {
            'email': request.user.email,
            'name': getattr(request.user, 'full_name', ''),
            'contact': getattr(request.user, 'contact_no', ''),
        }
        # print(user)
    except Exception as e:
        return redirect('/customer/login/')
    return render(request, "profile.html" , {'user': user})



def cart(request):
    if request.user.is_anonymous:
        return redirect("/customer/login/")
    try:
        username = {'user_name': request.user.email}
    except Exception as e:
        return redirect('/customer/login/')
    return render(request, "cart.html" ,username)
