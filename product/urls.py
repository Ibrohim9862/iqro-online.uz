from django.urls import path
from .views import CategoryProductListView,ProductDetial ,homeview,serachview,cantactview,addtocard,orderproduct,cartupdate,youcheckout
from . import views

urlpatterns = [
    path("", views.homeview , name="home"),
    path("product/<slug:category_slug>", CategoryProductListView.as_view(), name="catagory_product_list_view"),
    path("product/<slug:category_slug>/<slug:product_slug>", ProductDetial.as_view(), name="product_detail"),
    path("search", views.serachview, name="serach_view"),
    path("order", views.addtocard , name="add_to_card"),
    path("cartupdate", views.cartupdate , name="cart_update"),
    path("checkout", views.youcheckout, name="you_checkout"),
    path("order-product", views.orderproduct, name="order_product"),
    path("kantakt", views.cantactview, name="cantact_view"),
    path("delete", views.delete, name="delete_view")

]
