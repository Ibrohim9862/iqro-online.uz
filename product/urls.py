from django.urls import path
from .views import CategoryProductListView,ProductDetial ,homeview
from . import views

urlpatterns = [
    path("", views.homeview , name="home"),
    path("<slug:slug>", CategoryProductListView.as_view(), name="catagory_product_list_view"),
    path("<slug:slug>/<slug:product_slug", ProductDetial.as_view(), name="")
]
