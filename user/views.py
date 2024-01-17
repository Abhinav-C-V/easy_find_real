from django.shortcuts import render,redirect
from django.contrib import messages,auth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from listing.models import Listing
from .models import CustomUser
from listing.forms import AddPropertyForm

from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache


# Create your views here.

class UserSignupView(View):
    @method_decorator(never_cache)
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        # form = UserSignupForm()
        return render(request, 'accounts/register.html')
    
    @method_decorator(never_cache)
    def post(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        name = request.POST['name']
        email = request.POST['email']
        password_1 = request.POST['password_1']
        password_2 = request.POST['password_2']
        
        # Check if passwords match
        if password_1 == password_2:
            # Check if user already exists
            if CustomUser.objects.filter(email=email).exists():
                messages.error(request, 'Already registered with the email address')
                return redirect('user:register')
            else:
                # Determine user type based on the presence of the is_realtor checkbox
                is_realtor = request.POST.get('is_realtor')
                if is_realtor:
                    user = CustomUser.objects.create_realtor(email=email, name=name, password=password_1)
                else:
                    user = CustomUser.objects.create_user(email=email, name=name, password=password_1)
                
                # Login after Register
                # user = authenticate(request, username=email, password=password_1)
                # login(request, user)
                user.save()
                messages.success(request, 'You are now registered and can log in')                
                return redirect('user:login')

        else:
            return redirect('user:register')
            
            # return render(request, 'accounts/register.html')
        
class UserLoginView(View):
    @method_decorator(never_cache)
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('index')
        # form = UserLoginForm()
        return render(request, 'accounts/login.html')

    @method_decorator(never_cache)
    def post(self, request):
        if request.user.is_authenticated:
            return redirect('index')
        
        email = request.POST['email']
        password = request.POST['password']
        
        # Authenticate user
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('index')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('user:login')
            
        
def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'You have been logged out successfully.')
    return redirect('index')


class AddPropertyView(View):
    @method_decorator(never_cache)
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.is_realtor:
                return render(request, 'listings/add_property.html')
            messages.warning(request, 'Only realtors can add a property')
            return redirect('index')
        return redirect('user:login')
    
    @method_decorator(never_cache)
    def post(self, request):
        if request.user.is_authenticated:
            if request.user.is_realtor:
                title = request.POST.get('title')
                address = request.POST.get('address')
                city = request.POST.get('city')
                state = request.POST.get('state')
                zipcode = request.POST.get('zipcode')
                description = request.POST.get('description')
                price = request.POST.get('price')
                bedrooms = request.POST.get('bedrooms')
                bathrooms = request.POST.get('bathrooms')
                property_type = request.POST.get('property_type')
                property_area = request.POST.get('property_area')
                sale_type = request.POST.get('sale_type')
                photo_main = request.POST.get('photo_main')
                photo_1 = request.POST.get('photo_1','')
                photo_2 = request.POST.get('photo_2','')
                photo_3 = request.POST.get('photo_3','')
                # is_published = request.POST.get('is_published')
                is_published = request.POST.get('is_published') == 'on'
                # print(is_published)
                # print(property_type)
                
                if not title.strip() or not address.strip() or not city.strip() or not state.strip() or not zipcode.strip() or not description.strip():
                    messages.error(request, 'Please fill out all required fields.')
                    return redirect('user:add_property')
                
                try:
                    # Validate numeric fields
                    price = int(price)
                    bedrooms = int(bedrooms)
                    bathrooms = float(bathrooms)
                    property_area = int(property_area)
                    
                except ValueError:
                    print("Invalid numeric input for price")
                    messages.error(request, 'Invalid numeric input for price, bedrooms, or bathrooms.')
                    return redirect('user:add_property')
                
                if not photo_main:
                    messages.error(request, 'Main photo is required.')
                    return redirect('user:add_property')

                new_listing = Listing.objects.create(
                    realtor=request.user,
                    title=title,
                    city=city,
                    address=address,
                    state=state,
                    zipcode=zipcode,
                    description=description,
                    price=price,
                    bedrooms=bedrooms,
                    bathrooms=bathrooms,
                    property_type=property_type,
                    property_area=property_area,
                    sale_type=sale_type,
                    photo_main=photo_main,
                    photo_1=photo_1,
                    photo_2=photo_2,
                    photo_3=photo_3,
                    is_published=is_published
                )
                
                new_listing.save()
                print("Property added successfully")
                messages.success(request, 'Property added successfully')
                return redirect('user:add_property')
            else:
                messages.warning(request, 'Only realtors can add a property')
                return redirect('index')
        return redirect('user:login')
    
    
    
def user_dashboard(request):
    return render(request, 'accounts/dashboard.html')