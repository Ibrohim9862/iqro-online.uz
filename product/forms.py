from django import forms
from django.forms import fields, models
from .models import UsershopAdress

class UserShopAddressForms(forms.ModelForm):

    class Meta:
        model=UsershopAdress
        fields=('ism','familya','Address','phone','email','discription')