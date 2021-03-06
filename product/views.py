from django.conf.urls import url
from django.core.paginator import Paginator
from django.forms.forms import Form
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView,DetailView
from .forms import UserShopAddressForms
from django.db.models import Q
import telegram
from django.contrib import messages
from django.core.serializers.json import DjangoJSONEncoder
from django.core.serializers import serialize
from django.conf import Settings, settings



from .models import Banner, Books, Category, OrderItem, UsershopAdress



def yigindi_total(request):
    request.session['yigindi']=0
    for ham in request.session['cartdata'].keys():
        request.session['yigindi'] += request.session['cartdata'][str(ham)]['total']
    return request.session['yigindi']




def homeview(request):
    book_object=Books.objects
    banner=Banner.objects.all()
    yangilari=book_object.all().order_by('-id')[:10]
    biznes_boyicha=book_object.filter(catagory__name='Biznes va psixologiya').order_by('-id')[:10]
    jaxon_boyicha=book_object.filter(catagory__name='Jahon adabiyoti').order_by('-id')[:10]
    
    cart_p={}
    request.session['cartdata']=cart_p
    yigindi_total(request)
    context={
        'banners': banner,
        'yangilari':yangilari,
        'category_boyicha':biznes_boyicha,
        'jaxon_adabiyoti':jaxon_boyicha
    }
    return render(request, 'index.html' ,context)


class CategoryProductListView(ListView):
    model=Books
    template_name='shop-left-sidebar.html'
    context_object_name="product"
    paginate_by=15
        
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
            'kategoriya_boyicha':Books.objects.filter(catagory__slug=self.kwargs['category_slug']).exclude(slug=self.kwargs['product_slug'])[:15],
        })
        return context

    def get_object(self):
        query = get_object_or_404(Books,
        catagory__slug=self.kwargs['category_slug'],
        slug=self.kwargs['product_slug'])
        return query

def serachview(request):
    search_name=request.GET['search_name']
    product=Books.objects.filter(Q(name__icontains=search_name)|Q(auther__icontains=search_name)|Q(catagory__name__icontains=search_name)|Q(discription__icontains=search_name)).order_by('id')
    paginator = Paginator(product, 15) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context={
        'product':product,
        'page_obj':page_obj
    }
    return render(request,'shop-left-sidebar.html',context)


def addtocard(request,soni=1):
    
    
    product=Books.objects.get(id=request.GET['product_id'])
    
    cart_p={}
    cart_p[str(request.GET['product_id'])]={
        'nomi':product.name,
        'soni':soni,
        'image':product.image.url,  
        'narxi':product.narx,
        'total':product.narx * soni,
        'slug':product.slug,
        'cslug':product.catagory.slug
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
    
    if (str(request.GET['product_id']) in request.session['cartdata']) is not None:
        addtocard(request)

    if str(request.GET['product_id']) in request.session['cartdata']:
            cartdata=request.session['cartdata']
            cartdata[request.GET['product_id']]['soni'] = int(request.GET['soni'])
            cartdata[request.GET['product_id']]['total']=cartdata[request.GET['product_id']]['soni']*cartdata[request.GET['product_id']]['narxi']
            cartdata.update(cartdata)
            request.session['cartdata']=cartdata
    
    
    yigindi=yigindi_total(request)
    
    context={
        'data_session':request.session['cartdata'],
        'yigindi':yigindi
    }



    return JsonResponse({'data':context})


def delete(request):

    if str(request.GET['product_id']) in request.session['cartdata']:
            cartdata=request.session['cartdata']
            del cartdata[request.GET['product_id']]
            cartdata.update(cartdata)
            request.session['cartdata']=cartdata

    yigindi=yigindi_total(request)

    context={
        'data_session':request.session['cartdata'],
        'yigindi':yigindi
    }
    return JsonResponse({'data':context})


def cantactview(request):
    context={}  
    return render(request,'contact.html',context)



def orderproduct(request):
    
    return render(request,'shopping-cart.html')


def youcheckout(request):
    formt = UserShopAddressForms(request.POST or None)    
    if request.session['cartdata']: 
        if formt.is_valid():
            m=formt.save()        
            text='???????????:\t '+m.ism+' '+m.familya+'\n????\t: '+m.Address+'\n????\t: '+m.phone+'\n'
            text1=''
            for key,value1 in request.session['cartdata'].items():
                prduct=Books.objects.get(id=key)
                text1+="????:\t"+str(prduct)+"\n????:\t*"+str(value1['soni'])+"*\n"
                order=OrderItem()
                order.order=m
                order.product=prduct
                order.qauntity=value1['soni']
                order.save()
            text=text+text1+'\n????:\t'+str(request.session['yigindi'])+'so\'m'
            telegram_settings = settings.TELEGRAM
            bot = telegram.Bot(token=telegram_settings['bot_token'])
            bot.send_message(chat_id="@%s" % telegram_settings['channel_name'],
            text=text, parse_mode=telegram.ParseMode.HTML)

            del request.session['cartdata']
            del request.session['yigindi']
            request.session['cartdata']={}
            request.session['yigindi']=0
            messages.success(request,'Buyurtmangiz muvaffaqiyat bajarildi!')
            return redirect('home')
    context={'form':formt}
    return render(request,'checkout.html',context)

    

        
    


