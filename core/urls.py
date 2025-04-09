from django.urls import path
from core import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('',views.index,name='index'),
    path('add_product',views.add_product,name="add_product"),
    path('productdesc/<pk>',views.productdesc,name="productdesc"),
   path('add_to_cart/<pk>',views.add_to_cart,name="add_to_cart"),
   path('order_list',views.order_list,name="order_list"),
   path('add_item/<int:pk>',views.add_item,name="add_item"),
   path('remove_item/<int:pk>',views.remove_item,name="remove_item"),
    path("checkout_page", views.checkout_page, name="checkout_page"),
     path("payment", views.payment, name="payment"),


     path('confirm-order-cod/', views.confirm_order_cod, name='confirm_order_cod'),
     path('order-success/', views.order_success, name='order_success'),
   
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

