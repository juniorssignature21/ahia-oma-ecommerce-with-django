from django.shortcuts import render
from django.shortcuts import redirect, render
from django.contrib import messages
from django.db import models
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password

# from plugin.paginate_queryset import paginate_queryset
from store import models as store_models
from customer import models as customer_models


# Create your views here.
def custom_404_view(request):
    return render(request, "partials/404.html", status=404)

@login_required
def dashboard(request):
    orders = store_models.Order.objects.filter(customer=request.user)
    total_spent = store_models.Order.objects.filter(customer=request.user).aggregate(total=models.Sum("total"))["total"]
    notis  = customer_models.Notification.objects.filter(user=request.user, seen=False)
    
    context = {
        "orders":orders,
        "total_spent":total_spent,
        "notis":notis,
    }
    
    return render(request, "customer/dashboard.html", context)

@login_required
def orders(request):
    orders = store_models.Order.objects.filter(customer=request.user)
    
    context = {
        "orders":orders,
    }
    
    return render(request, "customer/orders.html", context)

@login_required
def order_detail(request, order_id):
    order = store_models.Order.objects.get(customer=request.user, order_id=order_id)
    
    context = {
        "order":order
    }
    
    return render(request, "customer/order_detail.html", context)

@login_required
def order_item_detail(request, order_id, item_id):
    order = store_models.Order.objects.get(customer=request.user, order_id=order_id)
    item  = store_models.OrderItem.objects.get(order=order, item_id=item_id)
    
    context = {
        "order":order,
        "item":item,
    }
    return render(request, "customer/order_item_detail.html", context)
    
