from django.shortcuts import render ,HttpResponse ,redirect, get_object_or_404
from home.models import Contact
from seller.models import Product
from django.contrib import messages

# Create your views here.

def index(request):
    products = Product.objects.prefetch_related('images').filter(is_active=True)
    return render(request, 'index.html', {'products': products})

def about(request):
    return render(request, 'about.html')

def contact(request):
    if request.method == "POST":
        fname = request.POST.get('fname')
        phone = request.POST.get('phone')
        email = request.POST.get('Email')
        subject = request.POST.get('subject')
        Message1 = request.POST.get('Message')
        contact = Contact(Full_name=fname,Email=email,Contact=phone,Subject=subject,Message=Message1)
        contact.save()
        print(fname,phone,email,subject,Message1)
        messages.success(request, 'Your message has been sent')
    return render(request, 'contact.html')

def download(request):
    return render(request, 'download.html')




def men(request):
    return render(request, 'men.html')

def women(request):
    return render(request, 'women.html')

def boy(request):
    return render(request, 'boy.html')

def girl(request):
    return render(request, 'girl.html')

def product_view(request, id):
    # product = get_object_or_404(Product, id=id)
    product = Product.objects.get(product_id = id)
    # product = get_object_or_404(Product, product_id=id)
    return render(request, 'product_view.html', {'product': product})