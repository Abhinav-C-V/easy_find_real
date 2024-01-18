from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages
from django.http import FileResponse, HttpResponse ,Http404
from django.utils.decorators import method_decorator
from django.urls import reverse
from . models import Listing
import random
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required

# Create your views here.
@never_cache
def index(request):
    properties = Listing.objects.all()
    random_property = random.choice(properties) if properties else None
    return render(request, 'index.html', {'random_property': random_property})

@never_cache
def about(request):
    properties = Listing.objects.all()
    random_property = random.choice(properties) if properties else None
    return render(request, 'about.html', {'random_property': random_property})


@never_cache
def contact(request):
    return render(request, 'contact.html')

@never_cache
def testimonial(request):
    return render(request, 'testimonial.html')

@never_cache
def property_list(request):
    if request.user.is_authenticated:
        properties = Listing.objects.all().order_by('-listing_date')

        search_keyword = request.GET.get('search_keyword', '')
        property_type = request.GET.get('property_type', '')
        location = request.GET.get('location', '')
        # print(search_keyword)
        # print(property_type)
        # print(location)
        
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

@never_cache
def property_agents(request):
    if request.user.is_authenticated:
        return render(request, 'properties/property-agent.html')
    return redirect(reverse('user:login'))
    

@never_cache
def property_types(request):
    if request.user.is_authenticated:
        return render(request, 'properties/property-type.html')
    return redirect(reverse('user:login'))

@never_cache
@login_required
def property_details(request):
    if request.user.is_authenticated:
        # if request.user.is_realtor:
        p_id = request.GET['p_id']
        try:
            single_property = Listing.objects.get(id=p_id)
        except Listing.objects.DoesNotExist:
            messages.warning(request, "Property does not exist")
            raise Http404("Property does not exist")
        if single_property.realtor == request.user:
            my_property = True
        my_property = False
        context = {
            'single_property':single_property,
            'my_property':my_property
        }
        print(single_property)
        return render(request, 'properties/property-details.html',context)
    return redirect(reverse('user:login'))
