from .models import Category

def category(request):
    categorys=Category.objects.all()
    return {'categorys':categorys}
