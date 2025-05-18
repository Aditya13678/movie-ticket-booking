from django.db import models
from bookings.models import Booking
from acc.models import user
# Create your models here.


class Payments(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    payment_method=models.CharField(max_length=100,
                                    choices=[['card','card'],['upi','upi'],['netbanking','netbanking']])
    amount = models.IntegerField()
    status = models.CharField(max_length=100,
                               choices=[['success','success'],['failed','failed']])
    
    transaction_time=models.DateTimeField(auto_now_add=True)
