from django.urls import path
from . import views


urlpatterns=[
    path('search/<slug>/',views.search_movie,name='search'),
   
]