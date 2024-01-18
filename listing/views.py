from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages
from django.http import FileResponse, HttpResponse ,Http404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from . models import Listing

# Create your views here.
def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')
 
def property_list(request):
    if request.user.is_authenticated:
        properties = Listing.objects.all().order_by('-listing_date')

        # Get the search parameters from the request
        search_keyword = request.GET.get('search_keyword', '')
        property_type = request.GET.get('property_type', '')
        location = request.GET.get('location', '')
        print(search_keyword)
        print(property_type)
        print(location)
        
        # Filter the properties based on the search parameters
        # if search_keyword:
        #     filtered_properties = properties.filter(title__icontains=search_keyword)
        #     if filtered_properties.exists():
        #         properties = filtered_properties
        # if property_type:
        #     filtered_properties = properties.filter(property_type__icontains=property_type)
        #     if filtered_properties.exists():
        #         properties = filtered_properties
        # if location:
        #     filtered_properties = properties.filter(state__icontains=location)
        #     if filtered_properties.exists():
        #         properties = filtered_properties
        if search_keyword:
            properties = properties.filter(title__icontains=search_keyword)
        if property_type:
            properties = properties.filter(property_type__icontains=property_type)
        if location:
            properties = properties.filter(state__icontains=location)

        context = {
            'properties': properties,
        }
        return render(request, 'properties/property-list.html', context)
    return redirect(reverse('user:login'))
    
def property_agents(request):
    if request.user.is_authenticated:
        return render(request, 'property-agent.html')
    return redirect(reverse('user:login'))
    
    
def property_types(request):
    if request.user.is_authenticated:
        return render(request, 'property-type.html')
    return redirect(reverse('user:login'))

def property_details(request):
    if request.user.is_authenticated:
        # if request.user.is_realtor:
        p_id = request.GET['p_id']
                
        single_property = Listing.objects.get(id=p_id)
        if single_property.realtor == request.user:
            my_property = True
        my_property = False
        context = {
            'single_property':single_property,
            'my_property':my_property
        }
        print(single_property)
        return render(request, 'properties/property-details.html',context)
    return redirect('user:login')

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
    
    

    
    
