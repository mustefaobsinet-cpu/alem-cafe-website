import uuid
from django.db import models
from django.utils import timezone

class SiteSettings(models.Model):
    cafe_name = models.CharField(max_length=120, default='Alem Cafe')
    phone_number = models.CharField(max_length=30, default='0913856409', help_text='Public phone number')
    sms_number = models.CharField(max_length=30, default='0913856409', help_text='Number customers see for order SMS/contact')
    telebirr_number = models.CharField(max_length=30, default='0913856407')
    address = models.CharField(max_length=255, default='HVQ8+H7R, Dire Dawa, Ethiopia')
    welcome_amharic = models.CharField(max_length=255, default='እንኳን ወደ አለም ካፌ በደህና መጡ')
    class Meta: verbose_name = 'Cafe settings'
    def __str__(self): return self.cafe_name
    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)
    @classmethod
    def get_settings(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

class PaymentMethod(models.Model):
    name = models.CharField(max_length=80, help_text='Example: Telebirr, CBE, Awash Bank, Abyssinia Bank')
    account_name = models.CharField(max_length=120, blank=True)
    account_number = models.CharField(max_length=80, blank=True)
    instructions = models.TextField(blank=True)
    active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)
    class Meta: ordering = ['sort_order','name']
    def __str__(self): return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)
    name_am = models.CharField(max_length=100, blank=True, verbose_name='Amharic name')
    sort_order = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)
    class Meta: ordering = ['sort_order','name']
    def __str__(self): return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
    name = models.CharField(max_length=120)
    name_am = models.CharField(max_length=120, blank=True, verbose_name='Amharic name')
    description = models.TextField(blank=True)
    description_am = models.TextField(blank=True, verbose_name='Amharic description')
    price = models.DecimalField(max_digits=9, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    available = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    class Meta: ordering = ['category__sort_order','name']
    def __str__(self): return self.name

class Order(models.Model):
    STATUS = [('pending','Pending payment review'),('accepted','Accepted'),('preparing','Preparing'),('ready','Ready'),('completed','Completed'),('cancelled','Cancelled')]
    order_number = models.CharField(max_length=14, unique=True, editable=False)
    customer_name = models.CharField(max_length=120)
    phone = models.CharField(max_length=30)
    order_type = models.CharField(max_length=20, choices=[('takeaway','Takeaway'),('dine_in','Dine in')])
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True, blank=True)
    payment_reference = models.CharField(max_length=120, blank=True, help_text='Transaction/reference number; owner verifies it manually')
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default='pending')
    payment_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    def save(self, *args, **kwargs):
        if not self.order_number: self.order_number = uuid.uuid4().hex[:10].upper()
        super().save(*args, **kwargs)
    @property
    def total(self): return sum((item.price * item.quantity for item in self.items.all()), start=0)
    def __str__(self): return f'{self.order_number} - {self.customer_name}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    product_name = models.CharField(max_length=120)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    def __str__(self): return f'{self.product_name} x {self.quantity}'

class ContactMessage(models.Model):
    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=30, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.name
