from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re

class CustomSelect(forms.Select):
    def __init__(self, choices, attrs=None):
        super().__init__(attrs)
        self.choices = choices

def validate_ifsc(value):
    if not re.match(r'^[A-Z]{4}0[A-Z0-9]{6}$', value):
        raise ValidationError(
            '%(value)s is not a valid IFSC code',
            params={'value': value},
        )

class MultipleFileTypeField(forms.FileField):
    def validate(self, value):
        super().validate(value)
        if value:
            file_types = ['application/pdf', 'image/jpeg', 'image/jpg']
            if value.content_type not in file_types:
                raise ValidationError(_('Invalid file type. Please upload a PDF, JPEG, or JPG file.'), code='invalid')


class S_Login(forms.Form):
    seller_id = forms.CharField(max_length=10, label='Seller Id', widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter Your Seller Id'}), validators=[RegexValidator(regex=r'^[0-9]*$', message='Only digits allowed')])
    email = forms.EmailField(label='Email', min_length=7, widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter Your Email'}))
    pass1 = forms.CharField(max_length=15, min_length=8, label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control form-control-pass','placeholder': 'Enter Your Password','id': 'password' ,'placeholder': 'Password' ,'required': 'required'}))


class S_Registration(forms.Form):
    fname = forms.CharField(max_length=40, min_length=3, label='Full Name', widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter Your Full Name'}))
    email = forms.EmailField(label='Email', min_length=7, widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter Your Email'}))
    aadhar = forms.CharField(max_length=12, min_length=12, label='Aadhar No', widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter Your Aadhar Number'}), validators=[RegexValidator(regex=r'^[0-9]*$', message='Only digits allowed')])
    contact = forms.CharField(max_length=10, min_length=3, label='Contact', widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter Your Contact Number'}), validators=[RegexValidator(regex=r'^[0-9]*$', message='Only digits allowed')])
    pass1 = forms.CharField(max_length=15, min_length=8, label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control form-control-pass','placeholder': 'Enter Your Password','id': 'password' ,'placeholder': 'Password' ,'required': 'required'}))
    pass2 = forms.CharField(max_length=15, min_length=8, label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Enter Your Confirm Password'}))

class OTP(forms.Form):
    otp = forms.CharField(max_length=6, min_length=6, label='Enter your email OTP', widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter Your OTP'}), validators=[RegexValidator(regex=r'^[0-9]*$', message='Only digits allowed')])

class f_OTP(forms.Form):
    otp = forms.CharField(max_length=6, min_length=6, label='Enter your email OTP', widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter Your OTP'}), validators=[RegexValidator(regex=r'^[0-9]*$', message='Only digits allowed')])
    password = forms.CharField(max_length=15, min_length=8, label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Enter Your Password','id': 'password','required': 'required'}))
    password2 = forms.CharField(max_length=15, min_length=8, label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Enter Your Confirm Password'}))

class Forgot_pass(forms.Form):
    email = forms.EmailField(label="Email Address", widget=forms.EmailInput(attrs={'class': 'form-control', 'id': 'email', 'placeholder': 'name@example.com', 'required': 'required'}))

class Personal_Info_form(forms.Form):
    seller_id = forms.CharField(max_length=10, label='Seller Id', widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter Your Seller Id'}), validators=[RegexValidator(regex=r'^[0-9]*$', message='Only digits allowed')])
    fname = forms.CharField(label='Full Name', widget=forms.TextInput(attrs={'class': 'form-control','readonly': 'true'}))
    ftname = forms.CharField(max_length=40, min_length=3, label='Father Name', widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter Your Father Name'}))
    gender = forms.ChoiceField(choices=[('Male', 'Male'),('Female', 'Female'),('Other', 'Other')], label="Gender", initial='Male', widget=forms.RadioSelect(attrs={'class': 'gender-form-label ms-5'}))
    dob = forms.DateField(label='DOB', widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    religion = forms.CharField(max_length=40, label='Religion', widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter Your Religion'}))
    haddress = forms.CharField(max_length=80, label='Home Address', widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter Your Home Address'}))
    hcountry = forms.CharField(label='Home Country' ,widget=CustomSelect(choices=(('','Select country'),), attrs={'class': 'form-control country', 'aria-label': 'Default select example', 'onchange': 'loadStates()'}))
    hstate = forms.CharField(label='Home State' ,widget=CustomSelect(choices=(('','Select State'),), attrs={'class': 'form-control state', 'aria-label': 'Default select example', 'onchange': 'loadCities()'}))
    hcity = forms.CharField(label='Home City' ,widget=CustomSelect(choices=(('','Select City'),), attrs={'class': 'form-control city', 'aria-label': 'Default select example'}))
    aadhar = forms.CharField(label='Aadhar No', widget=forms.TextInput(attrs={'class': 'form-control','readonly': 'true'}))
    pan_no = forms.CharField(max_length=10, min_length=10, label='Pan Card No', widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter Your Pan Number'}), validators=[RegexValidator(regex=r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$')])
    contact = forms.CharField(label='Contact', widget=forms.TextInput(attrs={'class': 'form-control','readonly': 'true'}))
    email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={'class': 'form-control','readonly': 'true'}))

class Business_Info_form(forms.Form):
    sname = forms.CharField(max_length=50, label='Shop Name', widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter Your Shop Name'}))
    saddress = forms.CharField(max_length=100, label='Shop Address', widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter Your Shop Address'}))
    bcountry = forms.CharField(label='Shop Country' ,widget=CustomSelect(choices=(('','Select country'),), attrs={'class': 'form-control country', 'aria-label': 'Default select example', 'onchange': 'loadStates()'}))
    bstate = forms.CharField(label='Shop State' ,widget=CustomSelect(choices=(('','Select State'),), attrs={'class': 'form-control state', 'aria-label': 'Default select example', 'onchange': 'loadCities()'}))
    bcity = forms.CharField(label='Shop City' ,widget=CustomSelect(choices=(('','Select City'),), attrs={'class': 'form-control city', 'aria-label': 'Default select example'}))
    gst = forms.CharField(max_length=15, min_length=15, label='GST No', widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter Your GST Number'}), validators=[RegexValidator(regex=r'^\d{2}[A-Z]{5}\d{4}[A-Z]{1}\d{1}Z\d{1}$', message='Only digits allowed')])

class Bank_Details_Form(forms.Form):
    Bhname = forms.CharField(max_length=50, label='Bank Account Holder Name', widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter Your Account Holder Name'}))
    bname = forms.CharField(label='Bank Name', widget=CustomSelect(choices=(('','Select Bank Name'),), attrs={'class': 'form-control'}))
    b_a_no = forms.CharField(max_length=18 ,min_length=9 ,label='Bank Account No' , widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter Your Account Number'}))
    ifsc = forms.CharField(max_length=11, min_length=11, label='IFSC Code',validators=[validate_ifsc], widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter Your Bank IFSC Number'}))

class Uplode_document_form(forms.Form):
    P_card = MultipleFileTypeField(label='Pan Card', required=False , widget=forms.FileInput(attrs={'class': 'form-control upload', 'accept': '.jpg,.jpeg,.pdf', 'required': 'true'}))
    A_card = MultipleFileTypeField(label='Aadhar Card', required=False , widget=forms.FileInput(attrs={'class': 'form-control upload', 'accept': '.jpg,.jpeg,.pdf', 'required': 'true'}))

class product(forms.Form):
    pname = forms.CharField(max_length=100,  label='Product Name', widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter Your Product Name'}))
    brand = forms.CharField(max_length=100,  label='Brand Name', widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter Your brand Name'}))
    price = forms.CharField(max_length=100,  label='Price', widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter Your product price'}))
    color = forms.CharField(max_length=100,  label='Color', widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter Your product color'}))
    size = forms.CharField(max_length=100,  label='Size', widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter Your product size'}))
    qty = forms.CharField(max_length=100,  label='Qty', widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter Your product qty'}))
    minfo = forms.CharField(label='More Details', widget=forms.Textarea(attrs={'class': 'form-control','placeholder': 'Enter Your More Details', 'rows': 4}))
