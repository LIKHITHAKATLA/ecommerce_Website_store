from django.contrib import admin # type: ignore
from core.models import *
# Register your models here.

admin.site.register(Customer)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(CheckoutAddress)
