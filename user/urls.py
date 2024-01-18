from django.urls import path,include
from . import views
from django.conf.urls.static import static
from django.conf import settings
from .views import UserLoginView, UserSignupView, AddPropertyView, EditPropertyView


urlpatterns = [
    # path('', views.index, name='user_index'),
    path('', UserLoginView.as_view(), name='login'),
    path('signup/', UserSignupView.as_view(), name='signup'),
    path('logout/', views.user_logout, name='logout'),
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
    path('realtor_property_details/', views.realtor_property_details, name='realtor_property_details'),
    path('add_property/', AddPropertyView.as_view(), name='add_property'),
    path('delete_property/', views.delete_property, name='delete_property'),
    path('edit_property/', EditPropertyView.as_view(), name='edit_property'),
    
    
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)