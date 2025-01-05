from django.contrib import admin
from django.urls import path
from seller import views

app_name = 'seller'

# seller urls
urlpatterns = [
    path("s_login/",views.s_login, name='s_login'),
    path("s_registration/",views.s_registration, name='s_registration'),
    path("s_otp/",views.s_otp, name='s_otp'),
    path("forgot_pass/",views.forgot_pass, name='forgot_pass'),
    path("f_otp/",views.f_otp, name='f_otp'),
    path("Personal_Information/",views.Personal_Information, name='Personal_Information'),
    path("Business_Information/",views.Business_Information, name='Business_Information'),
    path("Bank_Account_Details/",views.Bank_Account_Details, name='Bank_Account_Details'),
    path("Upload_Documents/",views.Upload_Documents, name='Upload_Documents'),
    path('temp/', views.temp, name='temp'),
    path("upload_products/",views.upload_products, name='upload_products'),
    path("home/",views.home, name='home'),
]