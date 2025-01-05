from django.shortcuts import render ,HttpResponse ,redirect
from django.contrib import messages
from .forms import S_Registration ,OTP ,f_OTP, Forgot_pass ,Personal_Info_form ,Business_Info_form ,Bank_Details_Form ,Uplode_document_form ,S_Login, product
from .signals import email_sender
from .models import S_User, SellerInformation
from django.utils import timezone
import random
from django.conf import settings
import os
import time
# Create your views here.

def temp(request):
    if request.method == 'POST':
        form = product(request.POST)
        if form.is_valid():
            print("passs")
            time.sleep(15)
            return redirect('/seller/temp/')
        else:
            print("not pass")
    else:
        form = product()
    return render(request, 'temp.html',{'form': form})

def s_login(request):
    if request.method == 'POST':
        form = S_Login(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            request.session['s_data'] = form.cleaned_data
            request.session.set_expiry(1800)
            Seller_Id = form.cleaned_data['seller_id']
            try:
                s_user = S_User.objects.get(Seller_Id=Seller_Id)
                if s_user.Password == form.cleaned_data['pass1']:
                    if s_user.Email == form.cleaned_data['email']:
                        try:
                            seller = SellerInformation.objects.get(Seller_Id=Seller_Id)
                            if seller.status == "valid":
                                messages.success(request, "You are successfully logged in.")
                                return redirect('/seller/home/')
                            elif seller.status == "invalid":
                                messages.warning(request, "your detils is invalid please try again. and fill this form.")
                                s_user = S_User.objects.get(Seller_Id=Seller_Id)
                                s_data = {"seller_id" : s_user.Seller_Id,"fname" : s_user.Full_name,"email" : s_user.Email,"aadhar" : s_user.Aadhar,"contact" : s_user.Contact}
                                request.session['s_data'] = s_data
                                return redirect('/seller/Personal_Information/')
                            else:
                                # print("your data is submited please waite and check befor three days")
                                messages.warning(request, "your data is submited please waite and check Validation Maile.")
                                return redirect('/seller/s_login/')
                        except:
                            messages.warning(request, "data is not store proparly please try again. and fill this form.")
                            s_user = S_User.objects.get(Seller_Id=Seller_Id)
                            s_data = {"seller_id" : s_user.Seller_Id,"fname" : s_user.Full_name,"email" : s_user.Email,"aadhar" : s_user.Aadhar,"contact" : s_user.Contact}
                            request.session['s_data'] = s_data
                            return redirect('/seller/Personal_Information/')
                    else:
                        messages.warning(request, "Email is Not Match Check Again")
                else:
                    messages.warning(request, "Your Password is encorrect.")
                    return redirect('/seller/s_login/')
            except:
                print("seller id is not found.")
    else:
        form = S_Login()
    return render(request, 'salesregistration/s_login.html',{'form': form})

def s_otp(request):
    if request.method == 'POST':
        form = OTP(request.POST)
        if form.is_valid():
            time.sleep(15)
            otp1 = request.session['otp1']
            otp = form.cleaned_data['otp']
            print(f"{otp},{otp1}")
            s_data = request.session.get('s_data', {})
            if str(otp1) == str(otp):
                S_User(Full_name = s_data.get('fname'),Email = s_data.get('email'),Aadhar = s_data.get('aadhar'),Contact = s_data.get('contact'),Password = s_data.get('pass1')).save()
                print(f"{s_data}")
                seller_id = S_User.objects.get(Email=s_data.get('email'))
                # email_sender(s_data.get('email'), 'Welcome to ShopingMart Platform', f'''\nHi {s_data.get('email')},\nthank you for registering at our site.\nyour seller id is created ucsess fully {seller_id.Seller_Id} \n\nthenks\nand\nvisit again''')
                # Here you can validate the OTP and process the data as needed
                # succsess(email)
                return redirect('/seller/Personal_Information/')
    else:
        form = OTP()
        context = {
            'form': form,
            'pagetitle': 'Seller Registraion',
            'formtitle': 'Sign up',
            'faction': '/seller/s_otp/',
            # 'infolink': '/seller/s_login/',
        }
    return render(request, 'salesregistration/s_registration.html',context)

def s_registration(request):
    if request.method == 'POST':
        form = S_Registration(request.POST)
        if form.is_valid():
            print(form.changed_data)
            request.session['s_data'] = form.cleaned_data
            # expiry_time = timezone.now() + timezone.timedelta(hours=1)
            # request.session.set_expiry(1800)
            email = form.cleaned_data['email']
            otp1 = random.randint(100000,999999)
            request.session['otp1'] = otp1
            try:
                otp = email_sender(email, "otp", f"hiiii your otp is {otp1}")
                # request.session['otp'] = otp1
            except Exception as e:
                print(f"error {e}")
            # Do something with the data (save to database, send email, etc.)
            return redirect('/seller/s_otp')
    else:
        form = S_Registration()
        context = {
            'form': form,
            'pagetitle': 'Seller Registraion',
            'formtitle': 'Sign up',
            'faction': '/seller/s_registration/',
            'infolink': '/seller/s_login/',
        }
    return render(request, 'salesregistration/s_registration.html',context)

def Personal_Information(request):
    # s_data = request.session.get('s_data', {})
    if request.method == 'POST':
        print("error 1")
        form = Personal_Info_form(request.POST)
        print("error 2")
        if form.is_valid():
                print(form.changed_data)
                request.session['P_info_data'] = form.cleaned_data
                print(request.session.get('P_info_data', {}))
                P_info_data = request.session.get('P_info_data', {})
                P_info_data['dob'] = P_info_data['dob'].strftime('%Y-%m-%d')
                print(request.session.get('P_info_data', {}))
                return redirect('/seller/Business_Information/')
        else:
            print("data is not valid")
            print(form.errors)
    else:
        # P_info_data = request.session.get('P_info_data')
        host_with_port = request.META.get('HTTP_HOST', '')
        referer = request.META.get('HTTP_REFERER', 'unknown')
        if referer == f'https://jemsmpatel.pythonanywhere.com/seller/s_otp/':
            s_data = request.session.get('s_data', {})
            form = Personal_Info_form(initial=s_data)
            context = {
                'form': form,
                'pagetitle': 'Seller Registraion',
                'formtitle': 'Personal Information',
                'faction': '/seller/Personal_Information/',
                'infolink': '/seller/s_login/',
            }
        elif referer == f'https://jemsmpatel.pythonanywhere.com/seller/s_login/':
            s_data = request.session.get('s_data', {})
            form = Personal_Info_form(initial=s_data)
            context = {
                'form': form,
                'pagetitle': 'Seller Registraion',
                'formtitle': 'Personal Information',
                'faction': '/seller/Personal_Information/',
                'infolink': '/seller/s_login/',
            }
        elif referer == f'https://jemsmpatel.pythonanywhere.com/seller/Business_Information/':
            P_info_data = request.session.get('P_info_data', {})
            form = Personal_Info_form(initial=P_info_data)
            context = {
                'form': form,
                'pagetitle': 'Seller Registraion',
                'formtitle': 'Personal Information',
                'faction': '/seller/Personal_Information/',
                'infolink': '/seller/s_login/',
            }
        elif referer == f'https://jemsmpatel.pythonanywhere.com/seller/Bank_Account_Details/':
            P_info_data = request.session.get('P_info_data', {})
            form = Personal_Info_form(initial=P_info_data)
            context = {
                'form': form,
                'pagetitle': 'Seller Registraion',
                'formtitle': 'Personal Information',
                'faction': '/seller/Personal_Information/',
                'infolink': '/seller/s_login/',
            }
        elif referer == f'https://jemsmpatel.pythonanywhere.com/seller/Upload_Documents/':
            P_info_data = request.session.get('P_info_data', {})
            form = Personal_Info_form(initial=P_info_data)
            context = {
                'form': form,
                'pagetitle': 'Seller Registraion',
                'formtitle': 'Personal Information',
                'faction': '/seller/Personal_Information/',
                'infolink': '/seller/s_login/',
            }
        else:
            return redirect('/seller/s_login/')
        print(f"Referer: {context}")
        return render(request, 'salesregistration/s_registration.html',context)
# initial=s_data
def Business_Information(request):
    if request.method == 'POST':
        form = Business_Info_form(request.POST)
        if form.is_valid():
            request.session['B_info_data'] = form.cleaned_data
            print("valid")
            return redirect('/seller/Bank_Account_Details/')
        else:
            print("data is not valid")
            print(form.errors)
    else:
        print("error 10")
        referer = request.META.get('HTTP_REFERER', 'unknown')
        host_with_port = request.META.get('HTTP_HOST', '')
        print("hiii")
        if referer == f'https://jemsmpatel.pythonanywhere.com/seller/Personal_Information/':
            B_info_data = request.session.get('B_info_data', {})
            form = Business_Info_form(initial=B_info_data)
            context = {
                'form': form,
                'pagetitle': 'Seller Registraion',
                'formtitle': 'Business Information',
                'faction': '/seller/Business_Information/',
                'infolink': '/seller/s_login/',
            }
        elif referer == f'https://jemsmpatel.pythonanywhere.com/seller/Bank_Account_Details/':
            B_info_data = request.session.get('B_info_data', {})
            form = Business_Info_form(initial=B_info_data)
            context = {
                'form': form,
                'pagetitle': 'Seller Registraion',
                'formtitle': 'Business Information',
                'faction': '/seller/Business_Information/',
                'infolink': '/seller/s_login/',
            }
        elif referer == f'https://jemsmpatel.pythonanywhere.com/seller/Upload_Documents/':
            B_info_data = request.session.get('B_info_data', {})
            form = Business_Info_form(initial=B_info_data)
            context = {
                'form': form,
                'pagetitle': 'Seller Registraion',
                'formtitle': 'Business Information',
                'faction': '/seller/Business_Information/',
                'infolink': '/seller/s_login/',
            }
        else:
            return redirect('/seller/s_login/')
    return render(request, 'salesregistration/s_registration.html',context)

def Bank_Account_Details(request):
    if request.method == 'POST':
        form = Bank_Details_Form(request.POST)
        if form.is_valid():
            request.session['B_Account_data'] = form.cleaned_data
            print("valid")
            return redirect('/seller/Upload_Documents/')
        else:
            print("data is not valid")
            print(form.errors)
    else:
        referer = request.META.get('HTTP_REFERER', 'unknown')
        host_with_port = request.META.get('HTTP_HOST', '')
        if referer == f'http://{host_with_port}/seller/Personal_Information/':
            B_Account_data = request.session.get('B_Account_data', {})
            form = Bank_Details_Form(initial=B_Account_data)
            context = {
                'form': form,
                'pagetitle': 'Seller Registraion',
                'formtitle': 'Business Information',
                'faction': '/seller/Bank_Account_Details/',
                'infolink': '/seller/s_login/',
            }
        elif referer == f'https://jemsmpatel.pythonanywhere.com/seller/Business_Information/':
            B_Account_data = request.session.get('B_Account_data', {})
            form = Bank_Details_Form(initial=B_Account_data)
            context = {
                'form': form,
                'pagetitle': 'Seller Registraion',
                'formtitle': 'Business Information',
                'faction': '/seller/Bank_Account_Details/',
                'infolink': '/seller/s_login/',
            }
        elif referer == f'https://jemsmpatel.pythonanywhere.com/seller/Upload_Documents/':
            B_Account_data = request.session.get('B_Account_data', {})
            form = Bank_Details_Form(initial=B_Account_data)
            context = {
                'form': form,
                'pagetitle': 'Seller Registraion',
                'formtitle': 'Business Information',
                'faction': '/seller/Bank_Account_Details/',
                'infolink': '/seller/s_login/',
            }
        else:
            return redirect('/seller/s_login/')
    return render(request, 'salesregistration/s_registration.html',context)

def Upload_Documents(request):
    if request.method == 'POST':
        form = Uplode_document_form(request.POST, request.FILES)
        if form.is_valid():
            print("passs1")
            P_info_data = request.session.get('P_info_data', {})
            B_info_data = request.session.get('B_info_data', {})
            B_Account_data = request.session.get('B_Account_data', {})
            print(f"Seller_Id={P_info_data.get('seller_id')},Father_Name={P_info_data.get('ftname')},Gender={P_info_data.get('gender')},Dob={P_info_data.get('dob')},Religion={P_info_data.get('religion')},Home_Address={P_info_data.get('haddress')},Home_Country={P_info_data.get('hcountry')},Home_State={P_info_data.get('hstate')},Home_City={P_info_data.get('hcity')},Pan_no={P_info_data.get('pan_no')},Shop_Name={B_info_data.get('sname')},Shop_Address={B_info_data.get('saddress')},Shop_Country={B_info_data.get('bcountry')},Shop_State={B_info_data.get('bstate')},Shop_City={B_info_data.get('bcity')},Gst={B_info_data.get('gst')},Bank_Account_Holder_Name={B_Account_data.get('Bhname')},Bank_Name={B_Account_data.get('bname')},Bank_Account_No={B_Account_data.get('b_a_no')},Bank_IFSC_Code={B_Account_data.get('ifsc')},P_card_copy={request.FILES.get('P_card')},A_card_copy={request.FILES.get('A_card')}")
            # try:
            seller_id = int(P_info_data.get('seller_id'))
            s_user = S_User.objects.get(Seller_Id=seller_id)
            S_U_Seller_Id = int(S_User.objects.get(Seller_Id=P_info_data.get('seller_id')).Seller_Id)
            print(S_U_Seller_Id)
            if S_U_Seller_Id == int(P_info_data.get('seller_id')):
                try:
                    seller_data = SellerInformation(Seller_Id=s_user,Father_Name=P_info_data.get('ftname'),Gender=P_info_data.get('gender'),Dob=P_info_data.get('dob'),Religion=P_info_data.get('religion'),Home_Address=P_info_data.get('haddress'),Home_Country=P_info_data.get('hcountry'),Home_State=P_info_data.get('hstate'),Home_City=P_info_data.get('hcity'),Pan_no=P_info_data.get('pan_no'),Shop_Name=B_info_data.get('sname'),Shop_Address=B_info_data.get('saddress'),Shop_Country=B_info_data.get('bcountry'),Shop_State=B_info_data.get('bstate'),Shop_City=B_info_data.get('bcity'),Gst=B_info_data.get('gst'),Bank_Account_Holder_Name=B_Account_data.get('Bhname'),Bank_Name=B_Account_data.get('bname'),Bank_Account_No=B_Account_data.get('b_a_no'),Bank_IFSC_Code=B_Account_data.get('ifsc'),P_card_copy=request.FILES.get('P_card'),A_card_copy=request.FILES.get('A_card'))
                    seller_data.save()
                    messages.success(request, f"Form Is Submmited Waite Three Days And Check Mails You Are Got A Validation Mail")
                    return redirect('/seller/s_login/')
                except S_User.DoesNotExist as e:
                    messages.error(request, f"Error :- {e}")
                    return redirect('/seller/Upload_Documents/')
                except Exception as e:
                    messages.error(request, f"Error :- {e}")
                    return redirect('/seller/Upload_Documents/')
            else:
                messages.error(request, "Seller Id Is Wrong Please Check Seller Id")
            # except S_User.DoesNotExist as e:
            #     print(e)
            # return redirect('/seller/Upload_Documents/')
        else:
            messages.error(request, "Invalid Form Please Try Again")
    else:
        referer = request.META.get('HTTP_REFERER', 'unknown')
        host_with_port = request.META.get('HTTP_HOST', '')
        if referer == f'https://jemsmpatel.pythonanywhere.com/seller/Personal_Information/':
            pass
        elif referer == f'https://jemsmpatel.pythonanywhere.com/seller/Business_Information/':
            pass
        elif referer == f'https://jemsmpatel.pythonanywhere.com/seller/Bank_Account_Details/':
            pass
        else:
            return redirect('/seller/s_login/')
        form = Uplode_document_form()
        context = {
                'form': form,
                'pagetitle': 'Seller Registraion',
                'formtitle': 'Business Information',
                'faction': '/seller/Upload_Documents/',
                'infolink': '/seller/s_login/',
            }
    return render(request, 'salesregistration/s_registration.html',context)

def upload_products(request):
    if request.method == 'POST':
        form = product(request.POST, request.FILES)
        if form.is_valid():
            print("passs1")
            if 'save_and_add_another' in request.POST:
                return redirect('/seller/upload_products/')  # Redirect to the same view to add another item
            else:
                return redirect('/seller/s_login/')   # Redirect to a list view or another page after saving
        else:
            print("not passs")
    else:
        referer = request.META.get('HTTP_REFERER', 'unknown')
        host_with_port = request.META.get('HTTP_HOST', '')
        if referer == f'http://{host_with_port}/seller/home/':
            form = product()
        elif referer == f'http://{host_with_port}/seller/upload_products/':
            form = product()
        else:
            return redirect('/seller/s_login/')
    return render(request, 'salesregistration/uploadproduct.html',{'form': form})

def home(request):
    form = 0
    return render(request, 'salesregistration/seller_home.html',{'form': form})

def forgot_pass(request):
    if request.method == 'POST':
        form = Forgot_pass(request.POST)
        if form.is_valid():
            email1 = form.cleaned_data['email']
            try:
                S_User.objects.get(Email = email1)
                print('user get')
                otp1 = random.randint(100000,999999)
                request.session['otp1'] = otp1
                request.session['user_email'] = email1
                try:
                    email_sender(email1, "otp", f"hiiii your otp is {otp1}")
                    messages.success(request, f'otp is sent on {email1}.')
                    print('mail sented')
                    return redirect('/seller/f_otp/')
                except Exception as e:
                    print(f"error {e}")
            except S_User.DoesNotExist:
                messages.error(request, 'user is not exist please sign up on this site.')
                return redirect('/seller/registration/')
    else:
        form = Forgot_pass()
        context = {
            'form': form,
            'pagetitle': 'Sign In',
            'formtitle': 'Forgot Password',
            'faction': '/seller/forgot_pass/',
            'infolink': '/seller/login/',
        }
    return render(request, 'forgot_pass.html', context)


def f_otp(request):
    if request.method == 'POST':
        form = f_OTP(request.POST)
        if form.is_valid():
            otp1 = request.session['otp1']
            email1 = request.session['user_email']
            otp = form.cleaned_data['otp']
            print(f"{otp},{otp1}")
            if form.cleaned_data['password'] == form.cleaned_data['password2']:
                if str(otp1) == str(otp):
                    user = S_User.objects.get(Email = email1)
                    user.Password = form.cleaned_data['password']
                    user.save()
                    messages.success(request, 'password has been changed succssesfully.')
                    return redirect('/seller/s_login/')
                else:
                    messages.error(request, 'otp is not match.please try again')
                    return redirect('/seller/forgot_pass/')
            else:
                messages.error(request, 'confirm password is not match please try again.')
                return redirect('/seller/forgot_pass/')
    else:
        form = f_OTP()
        context = {
            'form': form,
            'pagetitle': 'Seller Registraion',
            'formtitle': 'Forgot Password',
            'faction': '/seller/f_otp/',
            'infolink': '/seller/login/',
        }
    return render(request, 'forgot_pass.html', context)


