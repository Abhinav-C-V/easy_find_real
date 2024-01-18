from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages,auth
# from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from listing.models import Listing, Banner, PropertyType
from .models import CustomUser
from django.contrib.auth.hashers import check_password
from django.contrib.auth import update_session_auth_hash
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required


# Create your views here.

class UserSignupView(View):
    @method_decorator(never_cache)
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('index')
        # form = UserSignupForm()
        return render(request, 'accounts/register.html')
    
    @method_decorator(never_cache)
    def post(self, request):
        if request.user.is_authenticated:
            return redirect('index')
        name = request.POST['name']
        email = request.POST['email']
        password_1 = request.POST['password_1']
        password_2 = request.POST['password_2']
        
        if password_1 == password_2:
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
            

class UserLoginView(View):
    @method_decorator(never_cache)
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('index')
        return render(request, 'accounts/login.html')

    @method_decorator(never_cache)
    def post(self, request):
        if request.user.is_authenticated:
            return redirect('index')
        
        email = request.POST['email']
        password = request.POST['password']
        
        user = authenticate(request, username=email, password=password)
        
        if user is not None and user.is_active:
            login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('index')
        
        messages.error(request, 'Invalid login credentials')
        return redirect('user:login')
            
@never_cache
@login_required
def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'You have been logged out successfully.')
    return redirect('user:login')


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
                photo_main = request.FILES.get('photo_main')
                photo_1 = request.FILES.get('photo_1', None)
                photo_2 = request.FILES.get('photo_2', None)
                photo_3 = request.FILES.get('photo_3', None)
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
                
                if not photo_main or not photo_main.name.endswith(('.png', '.jpg', '.jpeg')):
                    messages.error(request, 'A valid main photo is required (PNG or JPG).')
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
    

@method_decorator(login_required, name='dispatch')
class EditPropertyView(View):
    @method_decorator(never_cache)
    def get(self, request):
        if request.user.is_authenticated and request.user.is_realtor:
            p_id=request.GET['p_id']
            listing = get_object_or_404(Listing, id=p_id, realtor=request.user)
            context = {
                'listing': listing
                }
            return render(request, 'listings/edit_property.html', context)
        messages.warning(request, 'You do not have permission to edit this property.')
        return redirect('user:login')
        
    @method_decorator(never_cache)
    def post(self, request):
        if request.user.is_authenticated and request.user.is_realtor:
            p_id=request.GET['p_id']
            listing = get_object_or_404(Listing, id=p_id, realtor=request.user)

            # Get the updated fields from the request
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
            photo_main = request.FILES.get('photo_main')
            photo_1 = request.FILES.get('photo_1', None)
            photo_2 = request.FILES.get('photo_2', None)
            photo_3 = request.FILES.get('photo_3', None)
            is_published = request.POST.get('is_published') == 'on'

            # Validate the fields
            if not title.strip() or not address.strip() or not city.strip() or not state.strip() or not zipcode.strip() or not description.strip():
                messages.error(request, 'Please fill out all required fields.')
                return redirect('user:edit_property')

            try:
                # Validate numeric fields
                price = int(price)
                bedrooms = int(bedrooms)
                bathrooms = float(bathrooms)
                property_area = int(property_area)
            except ValueError:
                messages.error(request, 'Invalid numeric input for price, bedrooms, or bathrooms.')
                return redirect('user:edit_property')

            if not photo_main or not photo_main.name.endswith(('.png', '.jpg', '.jpeg')):
                messages.error(request, 'A valid main photo is required (PNG or JPG).')
                return redirect('user:edit_property')

            listing.title = title
            listing.address = address
            listing.city = city
            listing.state = state
            listing.zipcode = zipcode
            listing.description = description
            listing.price = price
            listing.bedrooms = bedrooms
            listing.bathrooms = bathrooms
            listing.property_type = property_type
            listing.property_area = property_area
            listing.sale_type = sale_type
            listing.photo_main = photo_main
            listing.photo_1 = photo_1
            listing.photo_2 = photo_2
            listing.photo_3 = photo_3
            listing.is_published = is_published
            listing.save()

            messages.success(request, 'Property updated successfully')
            return redirect('user:user_dashboard')
        
        messages.warning(request, 'You do not have permission to edit this property.')
        return redirect('user:login')
      

@never_cache
@login_required
def delete_property(request):
    if request.user.is_authenticated and request.user.is_realtor:
        p_id=request.GET['p_id']
        Listing.objects.filter(id=p_id, realtor=request.user).delete()
        messages.success(request, 'Property deleted successfully')
        return redirect('index')
    messages.warning(request, 'You do not have permission to delete this property.')
    return redirect('user:login')

    
@never_cache
@login_required
def user_dashboard(request):
    if request.user.is_authenticated:
        if request.user.is_realtor:
            my_properties = Listing.objects.filter(realtor=request.user).order_by('-listing_date')
            context = {
                'my_properties':my_properties
            }
            print(my_properties)
        return render(request, 'accounts/dashboard.html',context)
    return redirect('user:login')

@never_cache
@login_required
def realtor_property_details(request):
    if request.user.is_authenticated:
        if request.user.is_realtor:
            p_id = request.GET['p_id']
                
            single_property = Listing.objects.get(id=p_id, realtor=request.user)
            context = {
                'single_property':single_property
            }
            print(single_property)
            return render(request, 'properties/realtor_property-details.html',context)
    return redirect('user:login')


@method_decorator(login_required, name='dispatch')
class EditPersonalInfoView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'accounts/edit_profile.html', {'user': request.user})
        return redirect('user:login')

    def post(self, request):
        if request.user.is_authenticated:
            name = request.POST['name']
            email = request.POST['email']
            password = request.POST['password']

            if not name.strip() or not email.strip():
                messages.error(request, 'Name and Email are required fields.')
                return redirect('user:edit_profile')
            
            # Check if the provided email already exists
            if CustomUser.objects.exclude(pk=request.user.pk).filter(email=email).exists():
                messages.error(request, 'Email already exists. Please choose a different email.')
                return redirect('user:edit_profile')
            
            # Verify the provided password
            if not check_password(password, request.user.password):
                messages.error(request, 'Incorrect password. Please enter the correct password.')
                return redirect('user:edit_profile')

            user = request.user
            user.name = name
            user.email = email
            user.save()

            messages.success(request, 'Your profile has been updated successfully')
            return redirect('user:user_dashboard')
        return redirect('user:login')
    
    
@method_decorator(login_required, name='dispatch')
class ChangePasswordView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'accounts/change_password.html')
        return redirect('user:login')

    def post(self, request):
        if request.user.is_authenticated:
            old_password = request.POST['password']
            new_password1 = request.POST['password_1']
            new_password2 = request.POST['password_2']

            if not check_password(old_password, request.user.password):
                messages.error(request, 'Incorrect old password. Please enter the correct password.')
                return redirect('user:change_password')

            if new_password1 != new_password2:
                messages.error(request, 'New passwords do not match. Please enter the same password in both fields.')
                return redirect('user:change_password')

            request.user.set_password(new_password1)
            request.user.save()

            # Important: update the session with the new password hash
            update_session_auth_hash(request, request.user)

            messages.success(request, 'Your password has been changed successfully')
            return redirect('user:user_dashboard')
        return redirect('user:login')
    
    
@never_cache
@login_required
def admin_dashboard(request):
    if request.user.is_authenticated and request.user.is_staff:
        properties = Listing.objects.all().order_by('-listing_date')
        banners = Banner.objects.all().order_by('-id')
        property_types = PropertyType.objects.all().order_by('-id')
        users = CustomUser.objects.all().order_by('-id')
        context = {
            'property_types':property_types,
            'banners':banners,
            'users':users,
            'properties':properties
        }
        # print(my_properties)
        return render(request, 'accounts/admin_dashboard.html',context)
    return redirect('user:login')

@never_cache
@login_required
def admin_deleteuser(request):
    if request.user.is_authenticated and request.user.is_staff:
        u_id=request.GET['u_id']
        CustomUser.objects.filter(id=u_id).delete()
        messages.warning(request, f'{user.name} is no longer a member')
        return redirect('user:admin_dashboard')
    return redirect('user:login')

@never_cache
@login_required
def admin_blockuser(request):
    if request.user.is_authenticated and request.user.is_staff:
        u_id=request.GET['u_id']
        block_check=CustomUser.objects.filter(id=u_id)
        for user in block_check:
            # print(user.is_active)
            if user.is_active:
                CustomUser.objects.filter(id=u_id).update(is_active=False)
                messages.warning(request, f'{user.name} is blocked')
            else:
                CustomUser.objects.filter(id=u_id).update(is_active=True)
                messages.success(request, f'{user.name} is unblocked')
            # print(user.is_active)
        return redirect('user:admin_dashboard')
    return redirect('user:login')
    

@never_cache
@login_required
def admin_delete_property(request):
    if request.user.is_authenticated and request.user.is_staff:
        p_id=request.GET['p_id']
        Listing.objects.filter(id=p_id).delete()
        messages.warning(request, 'property deleted successfully')
        return redirect('user:admin_dashboard')
    return redirect('user:login')

@never_cache
@login_required
def admin_deactivate_property(request):
    if request.user.is_authenticated and request.user.is_staff:
        p_id=request.GET['p_id']
        active_check=Listing.objects.filter(id=p_id)
        for pperty in active_check:
            # print(user.is_active)
            if pperty.is_published:
                Listing.objects.filter(id=p_id).update(is_published=False)
                messages.warning(request, 'property successfully deactivated')
            else:
                Listing.objects.filter(id=p_id).update(is_published=True)
                messages.success(request, f'property successfully activated')
            # print(user.is_active)
        return redirect('user:admin_dashboard')

    return redirect('user:login')