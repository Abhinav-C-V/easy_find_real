from django.shortcuts import render,redirect
from django.contrib import messages,auth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from .models import CustomUser
# from .forms import UserSignupForm

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
                return redirect('register')
            else:
                # Determine user type based on a form field (e.g., 'user_type')
                user_type = request.POST.get('user_type', 'normal')  # Default to normal user if not provided
                if user_type == 'realtor':
                    user = CustomUser.objects.create_realtor(email=email, name=name, password=password_1)
                else:
                    user = CustomUser.objects.create_user(email=email, name=name, password=password_1)
                
                # Login after Register
                # user = authenticate(request, username=email, password=password_1)
                # login(request, user)
                user.save()
                messages.success(request, 'You are now registered and can log in')
                return redirect('login')

        else:
            return render(request, 'accounts/register.html')
        
class UserLoginView(View):
    pass
            