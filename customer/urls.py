from django.urls import path
from customer import views

app_name = 'customer'
handler404 = "customer.views.custom_404_view"


urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("orders/", views.orders, name="orders"),
    path("order_detail/<order_id>/", views.order_detail, name="order_detail"),
    path("order_item_detail/<order_id>/<item_id>/", views.order_item_detail, name="order_item_detail"),
    
    path("wishlist/", views.wishlist, name="wishlist"),
    path("add_to_wishlist/<pk>/", views.add_to_wishlist, name="add_to_wishlist"),
    path("delete_wishlist/<pk>/", views.delete_wishlist, name="delete_wishlist"),
    
    path("notis/", views.notis, name="notis"),
    path("mark_notis_seen/<pk>/", views.mark_notis_seen, name="mark_notis_seen"),
    
    path("addresses/", views.addresses, name="addresses"),
    path("address_detail/<pk>/", views.address_detail, name="address_detail"),
    path("address_create/", views.address_create, name="mark_notis_seen"),
    path("address_delete/<pk>/", views.address_delete, name="address_delete"),
]

