from django import forms
from .models import search_movies_by_name

class Search_movie(forms.ModelForm):
    class Meta:
        model=search_movies_by_name
        fields='__all__'