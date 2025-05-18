from django.urls import path
from . import views

urlpatterns=[
    path('movielist/',views.movies_listview,name='movies_list'),
    path('yourorders/',views.your_orders,name='your_orders'),
    path('', views.home, name='home'),
    path('cancel/<int:booking_id>/', views.check_cancellation, name='cancel_booking')

]

