from django.urls import path,include
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('property_list/', views.property_list, name='property_list'),
    path('property_agents/', views.property_agents, name='property_agents'),
    path('property_types/', views.property_types, name='property_types'),
    path('property_details/', views.property_details, name='property_details'),
    path('testimonial/', views.testimonial, name='testimonial'),
    
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)