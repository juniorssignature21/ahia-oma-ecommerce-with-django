from django.shortcuts import render, redirect
from django.contrib import messages
from userauths.forms import UserRegistrationForm
from vendor import models as vendor_models
from userauths import models as userauths_models


from django.contrib.auth import authenticate, login, logout

# Create your views here.

def custom_404_view(request, exception):
    return render(request, '404.html', status=404)

def register_view(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in")
        return redirect("/")
    
    form = UserRegistrationForm(request.POST or None)
    
    if request.method == "POST" and form.is_valid():
        user = form.save()
        
        first_name = form.cleaned_data.get("first_name")
        last_name = form.cleaned_data.get("last_name")
        mobile = form.cleaned_data.get("mobile")
        email = form.cleaned_data.get("email")
        password1 = form.cleaned_data.get("password1")
        user_type = form.cleaned_data.get("user_type")
        
        full_name=f"{first_name} {last_name}"
        
        
        user = authenticate(email=email,password=password1)
        login(request, user)
        
        messages.success(request, "Account was created successfully")
        
        profile = userauths_models.Profile.objects.create(
            full_name=full_name,
            mobile=mobile,
            user=user,
        )
        if user_type == "Vendor":
            vendor_models.Vendor.objects.create(user=user, store_name=full_name)
            profile.user_Type= "Vendor"
        else:
            profile.user_Type = "Customer"
        
        profile.save()
        
        # next_url = request.GET.get("next", "store:index")
        return redirect("/")
    
    context = {
        "form": form
    }
    return render(request, "userauths/register.html", context)

def login_user(request):
    if request.user.is_authenticated:
        return redirect("/")
    
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        
        user = authenticate(email=email, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, "You have successfully logged in")
            # next_url = request.GET.get("next", "store:index")
            return redirect("/") 
        else:
            messages.info(request, "There was an error please try again!!!")
            return redirect("userauths:login_user")
        
    return render(request, "userauths/login.html")

def  logout_user(request):
    logout(request)
    return redirect("userauths:login_user")
        
