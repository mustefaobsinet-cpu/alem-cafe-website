from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from cafe import views
urlpatterns = [
 path('admin/', admin.site.urls),
 path('', views.home, name='home'),
 path('menu/', views.menu, name='menu'),
 path('cart/', views.cart, name='cart'),
 path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
 path('cart/update/<int:product_id>/', views.update_cart, name='update_cart'),
 path('checkout/', views.checkout, name='checkout'),
 path('order/<str:order_number>/', views.order_success, name='order_success'),
 path('owner/', views.owner_dashboard, name='owner_dashboard'),
 path('owner/settings/', views.owner_settings, name='owner_settings'),
 path('owner/orders/<int:order_id>/<str:status>/', views.update_order_status, name='update_order_status'),
 path('owner/account/', views.owner_account, name='owner_account'),
]
if settings.DEBUG:
 urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOTpath('temporary-owner-setup/', views.setup_owner_account, name='setup_owner_account'),)
