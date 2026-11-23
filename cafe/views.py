from decimal import Decimal
from urllib.parse import quote
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .models import Category, Product, Order, OrderItem, PaymentMethod, SiteSettings

def common(): return {'site': SiteSettings.get_settings()}
def home(request):
    products = Product.objects.filter(available=True, featured=True).select_related('category')[:6]
    return render(request, 'cafe/home.html', {**common(),'products':products})
def menu(request):
    categories = Category.objects.filter(active=True).prefetch_related('products')
    return render(request, 'cafe/menu.html', {**common(),'categories':categories})
def cart_data(request): return request.session.get('cart', {})
def cart(request):
    cart = cart_data(request); rows=[]; total=Decimal('0.00')
    for key, qty in cart.items():
        product = Product.objects.filter(pk=key, available=True).first()
        if product:
            subtotal = product.price * int(qty); total += subtotal; rows.append({'product':product,'quantity':int(qty),'subtotal':subtotal})
    return render(request,'cafe/cart.html',{**common(),'rows':rows,'total':total})
@require_POST
def add_to_cart(request, product_id):
    product=get_object_or_404(Product,pk=product_id,available=True); cart=cart_data(request); key=str(product.id); cart[key]=int(cart.get(key,0))+1; request.session['cart']=cart
    messages.success(request, f'{product.name} added to your cart / ወደ ቅርጫት ተጨምሯል')
    return redirect(request.POST.get('next') or 'menu')
@require_POST
def update_cart(request, product_id):
    cart=cart_data(request); qty=int(request.POST.get('quantity',1)); key=str(product_id)
    if qty <= 0: cart.pop(key,None)
    else: cart[key]=min(qty,50)
    request.session['cart']=cart; return redirect('cart')
@transaction.atomic
def checkout(request):
    cart=cart_data(request)
    if not cart: return redirect('menu')
    products={str(p.id):p for p in Product.objects.filter(id__in=cart.keys(),available=True)}
    if request.method=='POST':
        name=request.POST.get('customer_name','').strip(); phone=request.POST.get('phone','').strip(); method=get_object_or_404(PaymentMethod,pk=request.POST.get('payment_method'),active=True)
        if not name or len(phone)<7:
            messages.error(request,'Please enter your name and a valid phone number.'); return redirect('checkout')
        order=Order.objects.create(customer_name=name,phone=phone,order_type=request.POST.get('order_type','takeaway'),payment_method=method,payment_reference=request.POST.get('payment_reference','').strip(),notes=request.POST.get('notes','').strip())
        for key,qty in cart.items():
            p=products.get(key)
            if p: OrderItem.objects.create(order=order,product=p,product_name=p.name,price=p.price,quantity=min(int(qty),50))
        request.session['cart']={}
        return redirect('order_success',order_number=order.order_number)
    total=sum((products[k].price*int(q) for k,q in cart.items() if k in products),Decimal('0.00'))
    return render(request,'cafe/checkout.html',{**common(),'total':total,'methods':PaymentMethod.objects.filter(active=True)})
def order_success(request, order_number):
    order=get_object_or_404(Order,order_number=order_number)
    return render(request,'cafe/order_success.html',{**common(),'order':order})
@staff_member_required
def owner_dashboard(request):
    orders=Order.objects.prefetch_related('items').order_by('-created_at')[:50]
    return render(request,'cafe/owner.html',{**common(),'orders':orders,'pending':Order.objects.filter(status='pending').count(),'products':Product.objects.count()})
@staff_member_required
def owner_settings(request):
    # Settings and payment methods are edited through the protected Django admin.
    return render(request,'cafe/owner_settings.html',common())
@staff_member_required
@require_POST
def update_order_status(request, order_id, status):
    allowed={s for s,_ in Order.STATUS}
    if status in allowed:
        order=get_object_or_404(Order,pk=order_id)
        if status in ('accepted','preparing','ready','completed') and not order.payment_verified:
            messages.error(request,'Verify the payment first in the admin dashboard.'); return redirect('owner_dashboard')
        order.status=status; order.save(update_fields=['status'])
        messages.success(request,f'Order {order.order_number} updated to {status}.')
    return redirect('owner_dashboard')
@staff_member_required
def owner_account(request):
    if request.method=='POST':
        new_username=request.POST.get('username','').strip()
        form=PasswordChangeForm(request.user,request.POST)
        if not new_username:
            messages.error(request,'Username cannot be blank.')
        elif User.objects.exclude(pk=request.user.pk).filter(username__iexact=new_username).exists():
            messages.error(request,'That username is already in use.')
        elif form.is_valid():
            user=form.save(); user.username=new_username; user.save(update_fields=['username']); update_session_auth_hash(request,user); messages.success(request,'Username and password updated successfully.'); return redirect('owner_account')
    else: form=PasswordChangeForm(request.user)
    return render(request,'cafe/owner_account.html',{**common(),'form':form})
