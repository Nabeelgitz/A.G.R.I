from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('collect/', views.collect, name='collect'),
    path('processing/', views.processing, name='processing'),
    path('result/', views.result, name='result'),
    
    # ESP32 trigger
    path('trigger-collection/', views.trigger_collection, name='trigger_collection'),
    
    # API receive
    path('api/data/', views.receive_data, name='receive_data'),
    
    path(
    'download-report/',
    views.download_report,
    name='download_report'
),
]