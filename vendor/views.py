from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from store import models as store_models
from vendor import models as vendor_models
from django.db import models
from django.db.models.functions import TruncMonth

from django.contrib import messages
# Create your views here.

def get_monthly_sales():
    monthly_sales = (
        store_models.OrderItem.objects.annotate(month=TruncMonth("date"))
        .values("month")
        .annotate(order_count = models.Count("id"))
        .order_by("month")
    )

@login_required
def dashboard(request):
    products = store_models.Product.objects.filter(vendor=request.user)
    orders = store_models.Order.objects.filter(vendors=request.user)
    revenue = store_models.OrderItem.objects.filter(vendor=request.user).aggregate(total = models.Sum("total"))["total"]
    notifications = vendor_models.Notification.objects.filter(user=request.user, seen=False)
    reviews = store_models.Review.objects.filter(product__vendor=request.user)
    rating = store_models.Review.objects.filter(product__vendor=request.user).aggregate(avg = models.Avg("rating"))["avg"]
    monthly_sales = get_monthly_sales()
    
    context = {
        "products": products,
        "orders": orders,
        "revenue": revenue,
        "notifications": notifications,
        "reviews": reviews,
        "rating": rating,
        "monthly_sales": monthly_sales,
    }
    
    return render(request, "vendor/dashboard.html", context)
    
    
@login_required
def products(request):
    products = store_models.Product.objects.filter(vendor=request.user)
    
    context = {
        "products": products,
    }
    
    return render(request, "vendor/products.html", context)

@login_required
def orders(request):
    orders = store_models.Order.objects.filter(vendors=request.user)
    
    context = {
        "orders": orders,
    }
    
    return render(request, "vendor/orders.html", context)

@login_required
def order_detail(request, order_id):
    order = store_models.Order.objects.get(vendors=request.user,order_id=order_id)
    
    context = {
        "order": order,
    }
    
    return render(request, "vendor/order_detail.html", context)

@login_required
def order_item_detail(request, order_id, item_id):
    order = store_models.Order.objects.get(vendors=request.user,order_id=order_id, payment_status="Paid")
    item = store_models.OrderItem.objects.get(order=order, item_id=item_id)
    
    context = {
        "order": order,
        "item": item,
    }
    
    return render(request, "vendor/order_item_detail.html", context)
    

@login_required
def update_order_status(request, order_id):
    order = store_models.Order.objects.get(vendors=request.user,order_id=order_id, payment_status="Paid")
    if request.method == "POST":
        order.order_status = request.POST.get("status")
        order.save()
        
        messages.success(request, "Order Status Updated")
        return redirect("vendor:order_detail", order.order_id)
        
    return redirect("vendor:order_detail", order.order_id)

@login_required
def update_order_item_status(request, order_id, item_id):
    order = store_models.Order.objects.get(vendors=request.user,order_id=order_id, payment_status="Paid")
    item = store_models.OrderItem.objects.get(order=order, item_id=item_id)
    
    if request.method == "POST":
        order_status = request.POST.get("status")
        shipping_service = request.POST.get("shipping_service")
        tracking_id = request.POST.get("tracking_id")
        
        item.order_status = order_status
        item.shipping_services = shipping_service
        item.tracking_id = tracking_id
        item.save()
        
        messages.success(request, "Item Status Updated")
        return redirect("vendor:order_item_detail", order.order_id, item.item_id)
        
    return redirect("vendor:order_item_detail", order.order_id, item.item_id)