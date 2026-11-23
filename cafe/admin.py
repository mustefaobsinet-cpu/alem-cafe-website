from django.contrib import admin
from .models import SiteSettings, PaymentMethod, Category, Product, Order, OrderItem, ContactMessage
admin.site.site_header = 'Alem Cafe Owner Administration'
admin.site.site_title = 'Alem Cafe Admin'
admin.site.index_title = 'Manage your cafe'
@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = [('Cafe details', {'fields':('cafe_name','address','welcome_amharic')}),('Contact numbers', {'fields':('phone_number','sms_number','telebirr_number')})]
    def has_add_permission(self, request): return not SiteSettings.objects.exists()
@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin): list_display=('name','account_name','account_number','active','sort_order'); list_editable=('active','sort_order')
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin): list_display=('name','name_am','active','sort_order'); list_editable=('active','sort_order')
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin): list_display=('name','category','price','available','featured'); list_filter=('category','available'); search_fields=('name','name_am'); list_editable=('price','available','featured')
class OrderItemInline(admin.TabularInline): model=OrderItem; extra=0; readonly_fields=('product_name','price','quantity')
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin): list_display=('order_number','customer_name','phone','status','payment_verified','created_at'); list_filter=('status','payment_verified'); search_fields=('order_number','customer_name','phone'); inlines=[OrderItemInline]
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin): list_display=('name','phone','created_at'); search_fields=('name','phone')
