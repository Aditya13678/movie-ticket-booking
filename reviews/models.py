from django.db import models
from acc.models import user
from movies.models import Movie



# Create your models here.

class Review_table(models.Model):
    review_id=models.IntegerField(primary_key=True)
    user_id=models.ForeignKey(user,on_delete=models.CASCADE)
    movie=models.ForeignKey(Movie,on_delete=models.CASCADE)
    rating=models.DecimalField(max_digits=3,decimal_places=1)
    review_text=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    

