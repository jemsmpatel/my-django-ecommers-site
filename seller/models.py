import uuid
from django.db import models
from django.core.validators import RegexValidator
from django.utils.crypto import get_random_string
from .category import CATEGORYS  # Make sure CATEGORYS is correctly imported
from django.db.models import Max

# S_User Model: Seller information
class S_User(models.Model):
    # Define a function to generate a unique Seller_Id (using UUID)
    def generate_seller_id():
        return get_random_string(length=10, allowed_chars='0123456789')  # Generating a 10-character unique ID using UUID

    # Fields for the S_User model
    Seller_Id = models.CharField(
        primary_key=True,
        default=generate_seller_id,
        max_length=10,
        editable=False,  # Prevents editing of this field in forms
        unique=True      # Ensures uniqueness of Seller_Id
    )
    Full_name = models.CharField(max_length=255)
    Email = models.EmailField(unique=True)  # Unique constraint on Email
    Aadhar = models.CharField(max_length=12, validators=[RegexValidator(r'^\d{12}$')])  # Assuming Aadhar is 12 digits
    Contact = models.CharField(max_length=10, validators=[RegexValidator(r'^\+?1?\d{10}$')])  # Assuming Contact is a phone number
    Password = models.CharField(max_length=255)

    def __str__(self):
        return self.Seller_Id


# SellerInformation Model: Detailed seller information
class SellerInformation(models.Model):
    # Foreign key to connect with S_User table
    Seller_Id = models.OneToOneField(S_User, on_delete=models.CASCADE, primary_key=True)

    # Personal Information partition
    Father_Name = models.CharField(max_length=50)
    Gender = models.CharField(max_length=6)
    Dob = models.DateField()
    Religion = models.CharField(max_length=50)
    Home_Address = models.TextField()
    Home_Country = models.CharField(max_length=100)
    Home_State = models.CharField(max_length=100)
    Home_City = models.CharField(max_length=100)
    Pan_no = models.CharField(max_length=10, unique=True)

    # Business Information partition
    Shop_Name = models.CharField(max_length=150)
    Shop_Address = models.TextField()
    Shop_Country = models.CharField(max_length=100)
    Shop_State = models.CharField(max_length=100)
    Shop_City = models.CharField(max_length=100)
    Gst = models.CharField(max_length=15, unique=True)

    # Bank Account Details partition
    Bank_Account_Holder_Name = models.CharField(max_length=100)
    Bank_Name = models.CharField(max_length=100)
    Bank_Account_No = models.CharField(max_length=18, unique=True)
    Bank_IFSC_Code = models.CharField(max_length=11)

    # Uploaded Documents partition
    P_card_copy = models.ImageField(upload_to='pancard/')
    A_card_copy = models.ImageField(upload_to='aadharcard/')

    # Validation Status
    STATUS_CHOICES = [
        ('-----', '-----'),
        ('valid', 'Valid'),
        ('invalid', 'Invalid'),
    ]
    status = models.CharField(max_length=7, choices=STATUS_CHOICES, blank=False, default="-----")

    def __str__(self):
        return f"{self.Seller_Id.Full_name} - {self.Shop_Name}"


# Product Model: Information about products
class Product(models.Model):
    product_id = models.PositiveIntegerField(unique=True, editable=False, null=True, blank=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    mrp_price = models.CharField(max_length=10, validators=[RegexValidator(r'^\d+$', message="This field must contain only digits.")])
    price = models.CharField(max_length=10, validators=[RegexValidator(r'^\d+$', message="This field must contain only digits.")])
    discount_price = models.CharField(max_length=10, validators=[RegexValidator(r'^\d+$', message="This field must contain only digits.")], null=True, blank=True)
    category = models.CharField(max_length=100, choices=CATEGORYS, default='---', db_index=True)
    stock = models.PositiveIntegerField()
    sku = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    rating = models.FloatField(null=True, blank=True)
    brand = models.CharField(max_length=100, null=True, blank=True)
    tags = models.JSONField(null=True, blank=True)  # Requires Django 3.1+
    featured = models.BooleanField(default=False)

    # Foreign Key for linking a product with a seller
    seller = models.ForeignKey(S_User, related_name='products', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # Automatically set is_active to False when stock reaches 0
        if self.stock == 0:
            self.is_active = False

        # Assign product_id if not set
        if not self.product_id:
            max_id = Product.objects.aggregate(max_id=Max('product_id'))['max_id']
            self.product_id = (max_id or 0) + 1

        super(Product, self).save(*args, **kwargs)  # Call the parent class save method

    def __str__(self):
        return f"{self.name}  {self.product_id}"


# ProductImage Model: Multiple images for each product
class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return f"Image for {self.product.name}"
