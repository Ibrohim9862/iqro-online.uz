from django.contrib import admin
from .models import Category,Books,Banner,OrderItem,UsershopAdress

# admin.site.register(Category)
admin.site.register(Books)
admin.site.register(Banner)
admin.site.register(Category)
admin.site.register(OrderItem)
admin.site.register(UsershopAdress)
