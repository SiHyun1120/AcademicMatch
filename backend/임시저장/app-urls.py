#app-url.py
from django.contrib import admin
from django.urls import path

from app import views

urlpatterns = [
    path('', views.main, name = 'main'),
    path('listing/', views.listing, name = 'listing'),
    path('searching/', views.searching, name = 'searching'),
    
]
