from django.contrib import admin
from .models import Review_table

# Register your models here.

@admin.register(Review_table)

class reviewadmin(admin.ModelAdmin):

    list_display=['review_id','user_id','movie_id','rating','review_text','created_at']