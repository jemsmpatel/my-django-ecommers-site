from django.contrib import admin
from django.urls import path
from customer import views

app_name = 'customer'

# customer urls
urlpatterns = [
    path('registration/', views.registration, name='registration'),
    path("login/",views.loginuser, name='login'),
    path("forgot_pass/",views.forgot_pass, name='forgot_pass'),
    path("c_otp/",views.c_otp, name='c_otp'),
    path("logout/",views.logoutuser, name='logout'),
    path("cart/",views.cart, name='cart'),
    path("profile/",views.profile, name='profile'),
]