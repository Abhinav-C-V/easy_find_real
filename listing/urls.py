from django.urls import path,include
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('views.property_list/', views.property_list, name='property_list'),
    path('property_agents/', views.property_agents, name='property_agents'),
    path('property_types/', views.property_types, name='property_types'),
    
    
    
]