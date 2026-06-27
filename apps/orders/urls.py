from django.urls import path

from . import views

app_name = "orders"

urlpatterns = [
    path("cart/", views.cart, name="cart"),
    path("cart/add/<uuid:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/update/<uuid:product_id>/", views.update_cart_item, name="update_cart_item"),
    path("cart/remove/<uuid:product_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("cart/clear/", views.clear_cart, name="clear_cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("orders/<uuid:order_id>/", views.order_detail, name="detail"),
]
