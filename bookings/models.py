from django.db import models
from acc.models import user
from theater.models import Theaters,showtimes,Seats
# Create your models here.


class Booking(models.Model):
    user=models.ForeignKey(user,on_delete=models.CASCADE)
    showtime=models.ForeignKey(showtimes,on_delete=models.SET_NULL,null=True,blank=True)
    booking_time=models.DateTimeField(auto_now_add=True)
    total_amount=models.DecimalField(max_digits=10,decimal_places=2)
    booking_status=models.CharField(max_length=20,choices=[['confirmed','Confirmed'],['cancelled','Cancelled'],['oending','Pending']])


class BookingSeats(models.Model):
    booking=models.ForeignKey(Booking,on_delete=models.CASCADE)
    seat=models.ForeignKey(Seats,on_delete=models.SET_NULL,null=True,blank=True)