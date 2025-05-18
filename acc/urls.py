from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.registerview, name='register'),
    
    path('login/',views.sigin,name='login'),
    path('logout/',views.logoutview,name='logout'),
    
]