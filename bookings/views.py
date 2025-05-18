from django.shortcuts import render,redirect
from theater.models import Theaters,Seats,showtimes
from acc.models import user
from movies.models import Movie
from datetime import datetime,timedelta,date
import json

from userdashboard.views import check_cancellation
from .models import Booking,BookingSeats
from django.conf import settings
import stripe
from django.contrib.auth.decorators import login_required
from django.contrib import messages

stripe.api_key = settings.STRIPE_SECRET_KEY
# Create your views here.


def theater_show_time_view(request,slug):

    today=datetime.today().date()
    start_date=today-timedelta(days=0)
    week=[]
    for i in range(7):
        day=start_date+timedelta(days=i)
        week.append({
            'name':day.strftime("%a").upper(),
            'day':day.day,
            'month':day.strftime("%b").upper(),
            'date':day
        })



    if Movie.objects.filter(slug=slug).exists():
        movie=Movie.objects.get(slug=slug)
        theater_showtime=[
            showtimes.objects.filter(movie=movie,theater=theater).order_by('show_time')
            for theater in Theaters.objects.all()  if showtimes.objects.filter(movie=movie,theater=theater).exists()
        ]

        context={
            'theater_showtimes':theater_showtime,
            'name':movie,
            'week':week,
            'today':today,
            

            
        }

        return render(request,'theater/theater_showtimes_list.html',context)
    
    return render(request,'movies/404.html')




def theater_show_time_selected_date_view(request,slug,date_str):
    try:
        selected_date=datetime.strptime(date_str, '%Y-%m-%d').date()

    except ValueError:
        selected_date=datetime.today().date()
    today=datetime.today().date()
    start_date=today-timedelta(days=0)
    week=[]
    for i in range(7):
        day=start_date+timedelta(days=i)
        week.append({
            'name':day.strftime("%a").upper(),
            'day':day.day,
            'month':day.strftime("%b").upper(),
            'date':day
        })

    print(f"Movie slug: {slug}") 

    if Movie.objects.filter(slug=slug).exists():
        movie=Movie.objects.get(slug=slug)
        theater_showtimes=[
            showtimes.objects.filter(movie=movie,theater=theater,show_time__date=selected_date).order_by('show_time')
            for theater in Theaters.objects.all()  if showtimes.objects.filter(movie=movie,theater=theater,show_time__date=selected_date).exists()
        ]

        context={
            'theater_showtimes':theater_showtimes,
            'week':week,
            'today':today,
            'slug':slug,
            'selected_date': selected_date,
            'm':movie
        }
        return render(request,'theater/theater_showtimes_list.html',context)
    return render(request,'movies/404.html')
 





def seat_selection_view(request,showtime_id):
    showtime=showtimes.objects.get(id=showtime_id)
    all_seats=Seats.objects.filter(
        theater=showtime.theater,
        screen_number=showtime.screen_number
    ).order_by('row_label','seat_number')

    seat_rows={}
    for seat in all_seats:
        row=seat.row_label
        if row not in seat_rows:
            seat_rows[row]=[]
        seat_rows[row].append(seat)
    
    context={
        'showtime':showtime,
        'seat_rows':seat_rows,
        'st':showtime_id
    }

    return render(request,'theater/seating.html',context)




def book_ticket_view(request, showtime_id):
    if request.method == 'POST':
        # Check if 'selectedSeats' is in the POST data
        selected_seats = request.POST.get('selectedSeats')
        if not selected_seats:
            return render(request, 'movies/404.html', {'error': 'No seats selected'})
        
        # Parse the selected seats
        selected_seats = json.loads(selected_seats)
        
        # Calculate total amount
        total_amount = int(request.POST.get('total_amount', 0))
        tickets = []
        
        # Get the showtime object
        showtime = showtimes.objects.get(id=showtime_id)
        User = user.objects.get(username=request.user)

        # Create the booking
        booking = Booking.objects.create(
            user=User,
            showtime=showtime,
            total_amount=total_amount,
            booking_status='pending'
        )

        # Create BookingSeats for each selected seat
        for seat in selected_seats:
            tickets.append(seat['key'])
            seat_id = seat['id']
            seat_obj = Seats.objects.get(id=seat_id)
            BookingSeats.objects.create(
                booking=booking,
                seat=seat_obj
            )
        
        # Prepare the context for the payment page
        context = {
            'convenience_fee': 49,
            'showtime': showtime,
            'total_amount': total_amount,
            'sub_total': total_amount + 49,
            'tickets': tickets,
            'booking': booking,
            'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        }
        
        return render(request, 'payments/proceed_to_payment.html', context)

    return render(request, 'movies/404.html')


@login_required
def cancel_booking(request, booking_id):
    try:
        # Fetch the booking object using booking_id
        booking = Booking.objects.get(id=booking_id)
        
        # Pass booking_time to check_cancellation instead of booking_id
        if check_cancellation(booking.booking_time):
            # Proceed with cancellation if within the allowed time window
            booking.booking_status = 'cancelled'
            booking.save()
            
            # Delete associated seats
            BookingSeats.objects.filter(booking=booking).delete()
            
            # Show success message
            messages.success(request, "Booking Cancelled Successfully")
        else:
            # If cancellation window has expired
            messages.error(request, "Cancellation window has expired")
    
    except Booking.DoesNotExist:
        messages.error(request, "Booking not found")

    # Redirect back to 'your_orders' page
    return redirect('your_orders')
