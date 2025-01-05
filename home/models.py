from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone

# Custom Manager for User
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

# Custom User Model
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)  # email as primary identifier
    full_name = models.CharField(max_length=100, blank=True)
    contact_no = models.CharField(max_length=10, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)  # Automatically set to the current time
    last_login = models.DateTimeField(null=True, blank=True)  # Will be updated automatically on login

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'  # Make email the primary identifier
    REQUIRED_FIELDS = ['full_name']  # You can add any other fields here

    def __str__(self):
        return self.email

class Contact(models.Model):
    Full_name = models.CharField(max_length=255)
    Email = models.EmailField()
    Contact = models.CharField(max_length=10, validators=[RegexValidator(r'^\+?1?\d{10,10}$')])
    Subject = models.CharField(max_length=255)
    Message = models.TextField()
    date_joined = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.Email