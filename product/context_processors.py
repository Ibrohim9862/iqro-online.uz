from .models import Category,Books


def category(request):
    categorys=Category.objects.all()
    return {'categorys':categorys}
