from django.core.paginator import Paginator
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView,DetailView
from django.db.models import Q
# from django.template.loader import render_to_string



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
        
    def get_queryset(self):
        if self.kwargs.get('category_slug')=='all':
            product=Books.objects.all()
        elif self.kwargs.get('category_slug'):
            product=Books.objects.filter(catagory__slug=self.kwargs['category_slug'])               
        return product

class ProductDetial(DetailView):
    context_object_name="product"
    template_name='single-product.html'
    
    def get_context_data(self, **kwargs):
        context = super(ProductDetial, self).get_context_data(**kwargs)
        context.update({
            'kategoriya_boyicha':Books.objects.filter(catagory__slug=self.kwargs['category_slug']).exclude(slug=self.kwargs['product_slug'])[:15]
        })
        return   context

    def get_object(self):
        query = get_object_or_404(Books,
        catagory__slug=self.kwargs['category_slug'],
        slug=self.kwargs['product_slug'])
        return query

def serachview(request):
    search_name=request.GET['search_name']
    product=Books.objects.filter(Q(name__icontains=search_name)|Q(auther__icontains=search_name)|Q(catagory__name__icontains=search_name)|Q(discription__icontains=search_name))
    paginator = Paginator(product, 3) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context={
        'product':product,
        'page_obj':page_obj
    }
    return render(request,'shop-left-sidebar.html',context)


def yigindi_total(request):
    request.session['yigindi']=0
    for ham in request.session['cartdata'].keys():
        request.session['yigindi'] += request.session['cartdata'][str(ham)]['total']
    return request.session['yigindi']



def addtocard(request,soni=1):
    
    # request.session.clear()
    product=Books.objects.get(id=request.GET['product_id'])
    cart_p={}
    cart_p[str(request.GET['product_id'])]={
        'nomi':product.name,
        'soni':soni,
        'image':product.image.url,  
        'narxi':product.narx,
        'total':product.narx * soni
    }
    
    if 'cartdata' in request.session:
        if str(request.GET['product_id']) in request.session['cartdata']:
            cartdata=request.session['cartdata']
            cartdata[request.GET['product_id']]['soni'] += 1
            cartdata[request.GET['product_id']]['total']=cartdata[request.GET['product_id']]['soni']*cartdata[request.GET['product_id']]['narxi']
            cartdata.update(cartdata)
            request.session['cartdata']=cartdata
        else:
            cartdata=request.session['cartdata']
            cartdata.update(cart_p)
            request.session['product_id']=cartdata
    else:
        request.session['cartdata']=cart_p
   

    
    yigindi=yigindi_total(request)   
    context={
        'data_session':request.session['cartdata'],
        'yigindi':yigindi
    }
    return JsonResponse({'data':context})
 
def cartupdate(request):
    
    if str(request.GET['product_id']) in request.session['cartdata']:
            cartdata=request.session['cartdata']
            cartdata[request.GET['product_id']]['soni'] = request.GET['soni']
            cartdata[request.GET['product_id']]['total']=cartdata[request.GET['product_id']]['soni']*cartdata[request.GET['product_id']]['narxi']
            cartdata.update(cartdata)
            request.session['cartdata']=cartdata
    yigindi=yigindi_total(request)
    context={
        'data_session':request.session['cartdata'],
        'yigindi':yigindi
    }



    return JsonResponse(context)


def delete(request):

    if str(request.GET['product_id']) in request.session['cartdata']:
            cartdata=request.session['cartdata']
            del cartdata[request.GET['product_id']]
            cartdata.update(cartdata)
            request.session['cartdata']=cartdata

    print(cartdata)
    print(request.session['cartdata'])
    yigindi=yigindi_total(request)

    context={
        'data_session':request.session['cartdata'],
        'yigindi':yigindi
    }
    return JsonResponse({'data':context})


def cantactview(request):
    context=''
    return render(request,'contact.html',context)



def orderproduct(request):
    return render(request,'shopping-cart.html')


    

        
    


