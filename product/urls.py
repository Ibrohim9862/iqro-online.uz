from django.urls import path
from .views import CategoryProductListView,ProductDetial ,homeview,serachview
from . import views

urlpatterns = [
    path("", views.homeview , name="home"),
    path("product/<slug:category_slug>", CategoryProductListView.as_view(), name="catagory_product_list_view"),
    path("product/<slug:category_slug>/<slug:product_slug>", ProductDetial.as_view(), name="product_detail"),
    path("search", views.serachview, name="serach_view")
]
