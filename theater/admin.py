from django.contrib import admin
from .models import Theaters, showtimes, Seats
# Register your models here.

@admin.register(Theaters)
class theaterAdmin(admin.ModelAdmin):
    list_display=['id','name','city','address','manager']

@admin.register(showtimes)
class showtimesAdmin(admin.ModelAdmin):
    list_display=['id','movie_id','theater_id','show_time','screen_number']

@admin.register(Seats)
class SeatsAdmin(admin.ModelAdmin):
    list_display=['id','theater_id','screen_number','row_label','seat_number','seat_type']
  
