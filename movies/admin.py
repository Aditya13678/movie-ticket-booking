from django.contrib import admin
from .models import Movie

@admin.register(Movie)
# Register your models here.
class moviewAdmin(admin.ModelAdmin):
    list_display=['movie_id','title','genre','language','synopsis','cast','duration_minutes','release_date','thriller_url','status']
