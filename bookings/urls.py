from django.urls import path
from . import views

urlpatterns = [
    path('show_time/<slug>/',views.theater_show_time_view,name='showtime'),

    path('theatre_showtime/<slug:slug>/<str:date_str>/', views.theater_show_time_selected_date_view, name='theater_showtime_selected_date'),


    path('seating/<int:showtime_id>/',views.seat_selection_view,name='seating'),

    path("book_ticket/<int:showtime_id>/",views.book_ticket_view,name='book_ticket'),

    path('cancel/<int:booking_id>/',views.cancel_booking,name='cancel'),
]