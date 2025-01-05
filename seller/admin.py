from django.contrib import admin
from .models import S_User, SellerInformation, Product, ProductImage
from django.utils.html import format_html
from django import forms

# Register the S_User model
class S_UserAdmin(admin.ModelAdmin):
    list_display = ('Seller_Id', 'Full_name', 'Email', 'Contact', 'Aadhar')
    search_fields = ('Seller_Id', 'Full_name', 'Email')
    list_filter = ('Email',)

admin.site.register(S_User, S_UserAdmin)

# Register the SellerInformation model
@admin.register(SellerInformation)
class SellerInformationAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Personal Information', {
            'fields': ('Seller_Id', 'Father_Name', 'Gender', 'Dob', 'Religion', 'Home_Address', 'Home_Country', 'Home_State', 'Home_City', 'Pan_no')
        }),
        ('Business Information', {
            'fields': ('Shop_Name', 'Shop_Address', 'Shop_Country', 'Shop_State', 'Shop_City', 'Gst')
        }),
        ('Bank Account Details', {
            'fields': ('Bank_Account_Holder_Name', 'Bank_Name', 'Bank_Account_No', 'Bank_IFSC_Code')
        }),
        ('Uploaded Documents', {
            'fields': ('P_card_copy', 'display_p_card_copy', 'A_card_copy', 'display_a_card_copy')
        }),
        ('Validation', {
            'fields': ('status',)
        }),
    )

    list_display = ['Seller_Id', 'Shop_Name', 'status', 'display_p_card_copy', 'display_a_card_copy']
    search_fields = ['Seller_Id', 'Shop_Name', 'Home_City', 'Shop_City']
    list_filter = ['Home_Country', 'Shop_Country', 'status']
    ordering = ['Seller_Id']
    readonly_fields = ['display_p_card_copy', 'display_a_card_copy']

    def display_p_card_copy(self, obj):
        if obj.P_card_copy:
            return format_html('<img src="{}" width="100" height="100" />'.format(obj.P_card_copy.url))
        else:
            return 'No Image'
    display_p_card_copy.short_description = 'P Card Copy'

    def display_a_card_copy(self, obj):
        if obj.A_card_copy:
            return format_html('<img src="{}" width="100" height="100" />'.format(obj.A_card_copy.url))
        else:
            return 'No Image'
    display_a_card_copy.short_description = 'A Card Copy'

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == "status":
            kwargs['widget'] = forms.RadioSelect
        return super().formfield_for_choice_field(db_field, request, **kwargs)


# Inline Model for ProductImage
class ProductImageInline(admin.TabularInline):  # You can also use `admin.StackedInline`
    model = ProductImage
    extra = 1  # Number of empty forms to display by default
    fields = ('image', 'preview')
    readonly_fields = ('preview',)

    def preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 100px; height: auto;" />',
                obj.image.url
            )
        return "No Image"

    preview.short_description = "Preview"
# Register the Product model with Inline for ProductImage
class ProductAdmin(admin.ModelAdmin):
    list_display = ( 'name', 'product_id', 'price', 'category', 'stock', 'created_at', 'is_active')
    search_fields = ('name', 'sku', 'category')
    list_filter = ('category', 'is_active')
    inlines = [ProductImageInline]  # This will show ProductImage inline in Product's admin form

admin.site.register(Product, ProductAdmin)
