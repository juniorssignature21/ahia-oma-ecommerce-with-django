from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from store import models as store_models
from vendor import models as vendor_models
from django.db import models
from django.db.models.functions import TruncMonth
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
    
    
    
    
    
    