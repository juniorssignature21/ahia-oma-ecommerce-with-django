from django.urls import path

from userauths import views

# handler404 = 'your_app_name.views.custom_404_view'


app_name = "userauths"

urlpatterns = [
    path("sign_up/", views.register_view, name="sign_up"),
    path("login_user/", views.login_user, name="login_user"),
    path("logout_user/", views.logout_user, name="logout_user"),
]
