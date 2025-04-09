from django.shortcuts import render,redirect # type: ignore
from core.forms import *
from django.contrib import messages 
from core.models import *
from django.utils import timezone
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.shortcuts import render, get_object_or_404
from .models import Product
from django.http import HttpResponse
from .models import Order

# Create your views here.
def index(request):
    products = Product.objects.all()
    return render(request,'core/index.html',{'products':products})

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            # messages.success(request,"Product added susscesfully")
            return redirect('add_product')
        else:
            messages.info(request,"Product is not added,Try again")
        
    else:
        form = ProductForm()
    return render(request,'core/add_product.html',{'form':form})


def productdesc(request, pk):
    # Fetch the product based on its primary key (pk)
    product = Product.objects.get(pk=pk)
    return render(request, 'core/productdesc.html', {'product': product})

def add_to_cart(request, pk):
    # Get that Partiuclar Product of id = pk
    product = Product.objects.get(pk=pk)

    # Create Order item
    order_item, created = OrderItem.objects.get_or_create(
        product=product,
        user=request.user,
        ordered=False,
    )

    # Get Query set of Order Object of Particular User
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(product__pk=pk).exists():
            order_item.quantity += 1
            order_item.save()
            # messages.info(request, "Added Quantity Item")
            return redirect("productdesc", pk=pk)
        else:
            order.items.add(order_item)
            # messages.info(request, "Item added to Cart")
            return redirect("productdesc", pk=pk)

    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        # messages.info(request, "Item added to Cart")
        return redirect("productdesc", pk=pk)


def remove_item(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    
    if order_qs.exists():
        order = order_qs[0]
        
        if order.items.filter(product__pk=pk).exists():
            order_item = OrderItem.objects.filter(
                product=item,
                user=request.user,
                ordered=False,
            )[0]
            
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order_item.delete()
            
            # messages.info(request, "Item quantity updated")
        else:
            messages.info(request, "This item is not in your cart")
        
        return redirect("order_list")
    


def order_list(request):
    if Order.objects.filter(user=request.user, ordered=False).exists():
        order = Order.objects.get(user=request.user, ordered=False)
        return render(request, "core/order_list.html", {"order": order})
    return render(request, "core/order_list.html", {"message": "Your Cart is Empty"})



# core/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Product, Order, OrderItem

def add_item(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    # Fetch or create the order item
    order_item, created = OrderItem.objects.get_or_create(
        product=product,
        user=request.user,
        ordered=False,
    )
    
    # Get the active order for the user
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        
        # If the item is already in the cart, update the quantity
        if order.items.filter(product__pk=pk).exists():
            if order_item.quantity < product.product_available_count:
                order_item.quantity += 1
                order_item.save()
                # messages.info(request, "Increased item quantity")
            else:
                messages.info(request, "Sorry! Product is out of stock")
        else:
            order.items.add(order_item)
            # messages.info(request, "Item added to cart")
    else:
        order = Order.objects.create(user=request.user)
        Order.items.add(order_item)
        # messages.info(request, "Item added to cart")
    
    return redirect('order_list')  

def checkout_page(request):
    if CheckoutAddress.objects.filter(user=request.user).exists():
        return render(request, "core/checkout_address.html", {"payment_allow": "allow"})
    if request.method == "POST":
        # print("Saving must start")
        form = CheckoutForm(request.POST)
        if form.is_valid():
            street_address = form.cleaned_data.get("street_address")
            apartment_address = form.cleaned_data.get("apartment_address")
            country = form.cleaned_data.get("country")
            zip_code = form.cleaned_data.get("zip")

            checkout_address = CheckoutAddress(
                user=request.user,
                street_address=street_address,
                apartment_address=apartment_address,
                country=country,
                zip_code=zip_code,
            )
            checkout_address.save()
            # print("It should render the summary page")
            return render(
                request, "core/checkout_address.html", {"payment_allow": "allow"}
            )

    else:
        form = CheckoutForm()
        return render(request, "core/checkout_address.html", {"form": form})



def payment(request):
    order = Order.objects.filter(user=request.user, ordered=False).first()
    if order:
        # amount = get_final_price(Order)
        return render(request, 'core/payment.html')
    else:
        # messages.error(request, "No items in your cart!")
        return redirect('order_list')
    


from django.shortcuts import render, get_object_or_404
from .models import Order


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Order

def payment(request):
    # Get the active order for the user
    order = Order.objects.filter(user=request.user, ordered=False).first()
    
    if not order:
        # messages.error(request, "No items in your cart!")
        return redirect('order_list')

    # Calculate the total price
    total_price = sum(item.get_total_item_price() for item in order.items.all())

    # Render the payment page with total price
    return render(request, 'core/payment.html', {'order': order, 'total_price': total_price})

def confirm_order_cod(request):
    # Get the active order for the user
    order = Order.objects.filter(user=request.user, ordered=False).first()
    
    if not order:
        # messages.error(request, "No items in your cart!")
        return redirect('order_list')
    
    # Update the order status and payment method
    order.ordered = True
    order.payment_method = 'COD'
    order.ordered_date = timezone.now()
    order.save()

    # Clear the user's cart
    for item in order.items.all():
        item.ordered = True
        item.save()

    messages.success(request, "Your order has been placed successfully! Please pay on delivery.")
    return redirect('order_success')
from django.shortcuts import render

def order_success(request):
    return render(request, 'core/order_success.html')

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from .models import Product, Order, OrderItem

@login_required(login_url='login')
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)

    order_item, created = OrderItem.objects.get_or_create(
        product=product,
        user=request.user,
        ordered=False,
    )

    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(product__pk=pk).exists():
            order_item.quantity += 1
            order_item.save()
            # messages.info(request, "Added Quantity Item")
        else:
            order.items.add(order_item)
            # messages.info(request, "Item added to Cart")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        # messages.info(request, "Item added to Cart")

    return redirect("productdesc", pk=pk)



