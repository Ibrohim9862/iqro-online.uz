from django.contrib import admin
from .models import Category,Books,Banner,OrderItem,UsershopAdress

# admin.site.register(Category)


class BooksAtribute(admin.ModelAdmin):
    list_display=('name','catagory','narx','discription','image_tag','add_created_day')

admin.site.register(Books,BooksAtribute)


class BannerAtribute(admin.ModelAdmin):
    list_display=('banner','image_tag')

admin.site.register(Banner,BannerAtribute)



admin.site.register(Category)

class OrderItemAtribute(admin.ModelAdmin):
    list_display=('order','product','qauntity','date_added')

admin.site.register(OrderItem,OrderItemAtribute)



class UserShopAtribute(admin.ModelAdmin):
    list_display=('ism','familya','Address','phone','date_order')

admin.site.register(UsershopAdress,UserShopAtribute)
