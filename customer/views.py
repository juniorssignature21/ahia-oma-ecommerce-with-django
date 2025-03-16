from django.shortcuts import render
from django.shortcuts import redirect, render
from django.contrib import messages
from django.db import models
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse

# from plugin.paginate_queryset import paginate_queryset
from plugin.paginate_queryset import paginate_queryset
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


@login_required
def wishlist(request):
    wishlist_list = customer_models.Wishlist.objects.filter(user=request.user)
    # wishlist = paginate_queryset(request, wishlist_list, 1)
    
    context  = {
        "wishlist_list" : wishlist_list,
        # "wishlist" : wishlist,
    }
    return render(request, "customer/wishlist.html", context)

@login_required
def delete_wishlist(request, pk):
    wishlist_list  = customer_models.Wishlist.objects.get(user=request.user, id=pk)
    wishlist_list.delete()
    
    messages.success(request, "Item remove from wishlsit")
        
    return redirect("customer:wishlist")

@login_required
def add_to_wishlist(request, pk):
    if request.user.is_authenticated:
        product = store_models.Product.objects.filter(id=pk).first()
        wishlist_exist = customer_models.Wishlist.objects.filter(product=product, user=request.user).first()
        if not wishlist_exist: 
               
            customer_models.Wishlist.objects.create(
                user=request.user,
                product=product
            )    
        wishlist = customer_models.Wishlist.objects.filter(user=request.user)
        return JsonResponse({"message": "Item added to wishlist", "wishlist_count": wishlist.count()})
    else:
        return JsonResponse({"Message": "User is not logged in", "wishlist_count": "0"})
    

@login_required
def notis(request):
    notis_list = customer_models.Notification.objects.filter(user=request.user)
    unseen_notis_list = customer_models.Notification.objects.filter(user=request.user, seen=False)
    
    
    context={
        "notis_list":notis_list,
        "unseen_notis_list":unseen_notis_list,
    }
    
    return render(request, "customer/notis.html", context)

@login_required
def mark_notis_seen(request, pk):
    notis_list = customer_models.Notification.objects.get(user=request.user, id=pk,  seen=False)
    notis_list.seen=True
    
    notis_list.save()
    
    messages.success(request, "Notification marked as seen")
    return redirect("customer:notis")

@login_required
def addresses(request):
    addressess = customer_models.Address.objects.filter(user=request.user)
    
    context = {
        "addressess":addressess
    }
    return render(request, "customer/addresses.html", context)

@login_required
def address_detail(request, pk):
    address = customer_models.Address.objects.get(user=request.user, id=pk)
    
    if request.method == "POST":
        first_name = request.POST.get("fname") 
        last_name = request.POST.get("lname") 
        mobile = request.POST.get("mobile") 
        email = request.POST.get("email") 
        country = request.POST.get("country") 
        state = request.POST.get("state") 
        city = request.POST.get("city") 
        address_location = request.POST.get("address") 
        zip_code = request.POST.get("zip_code") 
        
        address.first_name = first_name
        
        address.first_name = first_name
        address.last_name = last_name
        address.mobile = mobile
        address.email = email
        address.country = country
        address.state = state
        address.address = address_location
        address.zip_code = zip_code
        
        address.save()
        
        messages.success(request, "Address Updated")
        return redirect("customer:address_detail", address.id)
    
    context = {
        "address":address
    }
    
    return render(request, "customer/address_detail.html", context)

@login_required
def address_create(request):
    if request.method == "POST":
        first_name = request.POST.get("fname") 
        last_name = request.POST.get("lname") 
        mobile = request.POST.get("mobile") 
        email = request.POST.get("email") 
        country = request.POST.get("country") 
        state = request.POST.get("state") 
        city = request.POST.get("city") 
        address_location = request.POST.get("address") 
        zip_code = request.POST.get("zip_code")
        
        customer_models.Address.objects.create(
            user=request.user,
            first_name=first_name,
            last_name=last_name,
            mobile=mobile,
            email=email,
            country=country,
            state=state,
            city=city,
            address=address_location,
            zip_code=zip_code, 
        )
        messages.success(request, "Address Created")
        return redirect("customer:addresses")
    
    
    return render(request, "customer/address_create.html")

@login_required
def address_delete(request, pk):
    address = customer_models.Address.objects.get(user=request.user, id=pk)
    address.delete()
    messages.success(request, "Address Delete")
    return redirect("customer:addresses")
    

@login_required
def customer_profile(request):
    profile = request.user.profile
    
    if request.method == "POST":
        image = request.FILES.get("image")
        full_name = request.POST.get("fname")
        mobile = request.POST.get("mobile")
        
        if image != None:
            profile.image = image
            
        profile.full_name = full_name
        profile.mobile = mobile#
        
        request.user.save()
        profile.save()
        
        messages.success(request, "Profile updated succesfully!!!")
        return redirect("customer:customer_profile")
    
    context = {
        "profile": profile
    }
    return render(request, "customer/profile.html", context)



@login_required
def change_password(request):
    if request.method == "POST":
        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        confirm_new_password = request.POST.get("confirm_new_password")
        
        if confirm_new_password != new_password:
            messages.error(request, "Passwords don't match!!!")
            return redirect(to="customer:change_password")
        
        if check_password(old_password, request.user.password):
            request.user.set_password(new_password)
            request.user.save()
            messages.success(request, "Passwords Changed Successfully!!")
            return redirect(to="customer:customer_profile")
        else:
            messages.error(request, "Old Password is Incorrect!!!")
            return redirect(to="customer:change_password")
        
    return render(request, "customer/change_password.html")
        