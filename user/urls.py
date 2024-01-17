from django.urls import path,include
from . import views
from django.conf.urls.static import static
from django.conf import settings
from .views import UserLoginView, UserSignupView, AddPropertyView


urlpatterns = [
    # path('', views.index, name='user_index'),
    path('', UserLoginView.as_view(), name='login'),
    path('signup/', UserSignupView.as_view(), name='signup'),
    path('logout/', views.user_logout, name='logout'),
    path('add_property/', AddPropertyView.as_view(), name='add_property'),
    
]