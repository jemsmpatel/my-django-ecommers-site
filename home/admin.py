from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Contact

# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'full_name', 'contact_no', 'is_active', 'is_staff', 'is_superuser')  # Changed to snake_case
    list_filter = ('is_staff', 'is_active', 'is_superuser')  # Changed to snake_case
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('full_name', 'contact_no')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active', 'is_superuser')}  # Changed to snake_case
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(User, CustomUserAdmin)



@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('Full_name', 'Email', 'Contact', 'Subject', 'date_joined')  # Fields to display in list view
    search_fields = ('Full_name', 'Email', 'Subject')  # Fields to search
    list_filter = ('date_joined',)  # Filters for list view
    ordering = ('-date_joined',)  # Order by date_joined (newest first)