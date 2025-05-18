from django.db import models
from acc.models import user
from movies.models import Movie
# Create your models here.
class Theaters(models.Model):
    name=models.CharField(max_length=200)
    city=models.CharField(max_length=200)
    address=models.CharField(max_length=2000)
    manager=models.ForeignKey(user,on_delete=models.SET_NULL , null=True , blank=True)


    

    def __str__(self):
        return self.name
    

    def generate_seats(self,screen_number,rows=['A','B','C','D','E','F','G','H','I','J'],seats_per_row=10):
        from .models import Seats


        for row in rows:
            if row in ['A','B','C']:
                seat_type='VIP'
            elif row in ['D','E','F']:
                seat_type='Gold'
            else:
                seat_type='Silver'

            for number in range(1,seats_per_row+1):
                Seats.objects.get_or_create(
                    theater=self,
                    screen_number=screen_number,
                    row_label=row,
                    seat_number=number,
                    defaults={'seat_type':seat_type}
                )




class showtimes(models.Model):

    movie=models.ForeignKey(Movie,on_delete=models.SET_NULL,null=True,blank=True)
    theater=models.ForeignKey(Theaters,on_delete=models.CASCADE)
    show_time=models.DateTimeField()
    screen_number=models.IntegerField(null=True,blank=True)

    

    def save(self,*args,**kwargs):
        is_new=self.pk is None
        super().save(*args,**kwargs)

        if is_new:
            self.theater.generate_seats(screen_number=self.screen_number)



class Seats(models.Model):
    theater=models.ForeignKey(Theaters,on_delete=models.CASCADE)
    screen_number=models.IntegerField(null=True,blank=True)
    row_label=models.CharField(max_length=10)
    seat_number=models.IntegerField()
    seat_type=models.CharField(max_length=20,choices=(('VIP','VIP'),('gold','Gold'),('silver','Silver')))

