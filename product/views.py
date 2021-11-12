from django.core import paginator
from django.shortcuts import redirect, render
from django.views.generic import ListView,DetailView

from .models import Banner, Books, Category







def homeview(request):
    book_object=Books.objects
    banner=Banner.objects.all()
    yangilari=book_object.all()[:10]
    biznes_boyicha=book_object.filter(catagory__name='Biznes va psixologiya')[:10]
    Jaxon_boyicha=book_object.filter(catagory__name='Jahon adabiyoti')[:10]
    
    context={
        'banners': banner,
        'yangilari':yangilari,
        'category_boyicha':biznes_boyicha,
        'jaxon_adabiyoti':Jaxon_boyicha
    }
    return render(request, 'index.html' ,context)


class CategoryProductListView(ListView):
    model=Books
    template_name='shop-left-sidebar.html'
    context_object_name="product"
    paginate_by=3
    
    def get_context_data(self, **kwargs):
        context = super(CategoryProductListView, self).get_context_data(**kwargs)
        context.update({
            'kateyory':Category.objects.all()
        })
        return context 
        
    def get_queryset(self):
        if self.kwargs.get('slug')=='all':
            product=Books.objects.all()
        elif self.kwargs.get('slug'):
            product=Books.objects.filter(catagory__slug=self.kwargs['slug'])               
        return product

class ProductDetial(DetailView):
    model = Books
    template_name=''
