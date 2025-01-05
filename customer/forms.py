from django import forms
from django.core.validators import RegexValidator


class OTP(forms.Form):
    otp = forms.CharField(max_length=6, min_length=6, label='Enter your email OTP', widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter Your OTP'}), validators=[RegexValidator(regex=r'^[0-9]*$', message='Only digits allowed')])
    password = forms.CharField(max_length=15, min_length=8, label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Enter Your Password','id': 'password','required': 'required'}))
    password2 = forms.CharField(max_length=15, min_length=8, label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Enter Your Confirm Password'}))


class Registration(forms.Form):
    fname = forms.CharField(max_length=40, min_length=3, label='Full Name', widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter Your Full Name'}))
    email = forms.EmailField(label='Email', min_length=7, widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter Your Email'}))
    contact = forms.CharField(max_length=10, min_length=10, label='Contact', widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter Your Contact Number'}), validators=[RegexValidator(regex=r'^[0-9]*$', message='Only digits allowed')])
    password = forms.CharField(max_length=15, min_length=8, label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Enter Your Password','id': 'password','required': 'required'}))
    password2 = forms.CharField(max_length=15, min_length=8, label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Enter Your Confirm Password'}))

class Login(forms.Form):
    email = forms.EmailField(label="Email Address", widget=forms.EmailInput(attrs={'class': 'form-control', 'id': 'email', 'placeholder': 'name@example.com', 'required': 'required'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control' ,'id': 'password' ,'placeholder': 'Password' ,'required': 'required'}))

class Forgot_pass(forms.Form):
    email = forms.EmailField(label="Email Address", widget=forms.EmailInput(attrs={'class': 'form-control', 'id': 'email', 'placeholder': 'name@example.com', 'required': 'required'}))
