from django.db import models
from django.db.models.deletion import CASCADE
from django.utils.html import mark_safe
from django.db.models.signals import pre_save
from books.utils import unique_slug_generator
from django.urls import reverse

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)
    slug=models.SlugField(max_length=120,blank=True,null=True)

    def __str__(self):
        return self.name
    
    def image_tag(self):
        return mark_safe('<img src="%s" width="80" heigth="60">' % (self.image.url))  

class Books(models.Model):
    name = models.CharField(max_length=60)
    auther=models.CharField(max_length=60,default="Unicon")
    image=models.ImageField(upload_to='books/')
    narx=models.IntegerField()
    catagory=models.ForeignKey(Category, on_delete=models.CASCADE)
    slug=models.SlugField(max_length=120,blank=True,null=True)
    discription = models.TextField(null=True, blank=True)
    add_created_day=models.DateField(auto_now=True)
    book_add_day=models.DateField(auto_now_add=True)

    def image_tag(self):
        return mark_safe('<img src="%s" width="80" heigth="60">' % (self.image.url))

    def __str__(self):
        return self.name


class Banner(models.Model):
    banner=models.ForeignKey(Books,on_delete=models.CASCADE)
    image=models.ImageField(upload_to='banner/')

    
class UsershopAdress(models.Model):
    name = models.CharField(max_length=100)
    Address=models.CharField(max_length=200)
    phone=models.CharField(max_length=15)
    email=models.EmailField(max_length=50,blank=True,null=True)
    date_order=models.DateField(auto_now_add=True)
    complate=models.BooleanField(default=False)
    
    def __str__(self):
        return self.name


class OrderItem(models.Model):
    order = models.ForeignKey(UsershopAdress,on_delete=models.CASCADE)
    product=models.ForeignKey(Books,on_delete=models.SET_NULL, null=True)
    qauntity= models.IntegerField()
    date_added=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product


def slug_genrator(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug =unique_slug_generator(instance)

pre_save.connect(slug_genrator,sender=Books)
pre_save.connect(slug_genrator,sender=Category)
