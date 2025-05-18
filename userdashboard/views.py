from django.shortcuts import render, redirect
from movies.models import Movie
from acc.models import user
from bookings.models import Booking, BookingSeats
from payments.models import Payments
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from datetime import timedelta
from django.contrib import messages

# View for displaying the list of movies
def movies_listview(request):
    context = {
        'movies': Movie.objects.all()
    }
    return render(request, 'movies/movie_list.html', context)

# View for showing user's confirmed bookings and their respective details
@login_required
def your_orders(request):
    User = request.user
    bookings = Booking.objects.filter(user=request.user, booking_status='confirmed').order_by('-booking_time')
    tickets = {
        Payments.objects.filter(booking=booking).first(): (
            BookingSeats.objects.filter(booking=booking), check_cancellation(booking_time=booking.booking_time))
        for booking in bookings
    }
    context = {
        'movies': Movie.objects.all(),
        'tickets': tickets,
        'user': User,
    }
    return render(request, 'userdashboard/your_orders.html', context)

# Cancellation check function (only allows cancellation within 20 minutes of booking time)
def check_cancellation(booking_time):
    return now() - booking_time <= timedelta(minutes=20)

# View to handle the home page where all movies are shown
def home(request):
    log = Movie.objects.all()
    return render(request, 'accounts/home.html', {'movies': log})

# View for handling the cancellation of bookings
@login_required
def cancel_booking(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id)
    except Booking.DoesNotExist:
        messages.error(request, "Booking not found")
        return redirect('your_orders')

    # Check if cancellation is within the allowed time frame
    if check_cancellation(booking_time=booking.booking_time):
        booking.booking_status = 'cancelled'
        booking.save()
        BookingSeats.objects.filter(booking=booking).delete()
        messages.success(request, "Booking Cancelled Successfully")
    else:
        messages.error(request, "Cancellation window has expired")

    return redirect('your_orders')

