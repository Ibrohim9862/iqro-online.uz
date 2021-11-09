from django.shortcuts import render


def homeview(request):
    context={}
    return render(request, 'index.html' ,context)