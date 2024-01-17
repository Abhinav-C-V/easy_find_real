from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages
from django.http import FileResponse, HttpResponse ,Http404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.core.files.storage import FileSystemStorage

# Create your views here.
def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')
 
def property_list(request):
    return render(request, 'property-list.html')
    
def property_agents(request):
    return render(request, 'property-agent.html')
    
def property_types(request):
    return render(request, 'property-type.html')
@never_cache
def index(request):
    # if 'user_email' in request.session:
    return render(request, 'index.html')
    # else:
    #     cat=Category.objects.all()
    #     cat_id = request.GET.get('cat_id')
    #     prod = request.GET.get('prod_id')
    #     if cat_id is not None and prod is None:
    #         details3= Variation.objects.filter(product__category__id=cat_id).order_by('id')
    #     elif prod is not None and cat_id is None:
    #         details3= Variation.objects.filter(product__product_name__icontains=prod).order_by('id')
    #     elif prod is not None and cat_id is not None:
    #         details3= Variation.objects.filter(product__product_name__icontains=prod,product__category__id=cat_id).order_by('id')
    #     else:
    #         details3=Variation.objects.all().order_by('id')
    #     popular_pdt=details3.order_by('id')[:4]
    #     new_arivals=details3.order_by('-id')[:4]
    #     recommended = details3.order_by('product')[:4]
        
    #     obj = Banner.objects.all()
    #     context={ 
    #             # 'page_obj': page_obj,
    #             'cat':cat,
    #             'obj':obj,
    #             'new_arivals':new_arivals,
    #             'popular_pdt':popular_pdt,
    #             'recommended':recommended,
    #         }
    #     return render(request, 'index.html',context )
    
    

    
    
