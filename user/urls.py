from django.urls import path,include
from . import views
from django.conf.urls.static import static
from django.conf import settings
from .views import UserLoginView, UserSignupView, AddPropertyView, EditPropertyView, EditPersonalInfoView, ChangePasswordView


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
    path('edit_personalinfo/', EditPersonalInfoView.as_view(), name='edit_personalinfo'),
    path('change_password/', ChangePasswordView.as_view(), name='change_password'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin_blockuser/', views.admin_blockuser, name='admin_blockuser'),
    path('admin_deleteuser/', views.admin_deleteuser, name='admin_deleteuser'),
    path('admin_deactivate_property/', views.admin_deactivate_property, name='admin_deactivate_property'),
    path('admin_delete_property/', views.admin_delete_property, name='admin_delete_property'),
    
    
    
    
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)