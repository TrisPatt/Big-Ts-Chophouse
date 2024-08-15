from django.shortcuts import render, redirect, get_object_or_404
from django.db import models
from .models import Reservation, Table
from .forms import ReservationForm, CancelReservationForm
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Count
from django.contrib.auth.decorators import login_required


# home page
def home(request):
    return render(request, 'reservation/home.html')

# Confirmed reservation
def reservation_confirmed(request, reservation_number):
    reservation = get_object_or_404(Reservation, pk=reservation_number)
    return render(request, 'reservation/reservation_confirmed.html', {'reservation': reservation})

#review reservations
@login_required #Only allow logged in users to view reservation with their unique id
def reservation_list(request):
    if request.user.is_authenticated:
        reservations = Reservation.objects.filter(user_id=request.user.id)
        return render(request, 'reservation/reservation_list.html', {'reservations': reservations})
    else:
        # Redirect to login page if the user is not authenticated
        return redirect('templates/account/login.html') 


@login_required #Only allow logged in users to create a reservation with their unique id
def reservation_create(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user_id = request.user
            reservation.save()

            num_guests = reservation.number_of_guests
            tables_needed = (num_guests + 1) // 2  # Calculate how many tables of 2 are needed

            # Calculate available tables on a partcular date and time
            available_tables = Table.objects.annotate(
                reserved_count=models.Count('reservations', filter=models.Q(
                    reservations__date=reservation.date,
                    reservations__time=reservation.time,
                    reservations__reservation_status=0
                ))
            ).filter(reserved_count=0).count()

            if tables_needed <= available_tables:
                tables = Table.objects.annotate(
                    reserved_count=models.Count('reservations', filter=models.Q(
                        reservations__date=reservation.date,
                        reservations__time=reservation.time,
                        reservations__reservation_status=0
                    ))
                ).filter(reserved_count=0)[:tables_needed]

                reservation.tables.add(*tables)
                reservation.save()
                
                #sends email to user- set as backend to display in console during dev
                send_mail(
                'Reservation Confirmed !',
                f'Your reservation on {reservation.date} at {reservation.time} has been successfully booked.',
                settings.DEFAULT_FROM_EMAIL,
                [request.user.email],
                fail_silently=False,
                )
                return redirect('reservation_confirmed', reservation_number=reservation.pk)

            else:
                messages.error(request, "Sorry, we can't accommodate your party size at the requested time.")
                return redirect('reservation_create')
    else:
        form = ReservationForm()

    return render(request, 'reservation/reservation_form.html', {'form': form})

@login_required # Cancel reservations once logged in
def cancel_reservation(request, reservation_number):
    # Fetch the reservation based on the reservation_number and ensure the user is authorized
    reservation = get_object_or_404(Reservation, reservation_number=reservation_number, user_id=request.user)
    
    if request.method == 'POST':
        form = CancelReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            reservation.reservation_status = 1 #update status to cancelled
            form.save() # Save the reservation with the new status
            messages.success(request, 'Your reservation has been successfully cancelled.') # Display confirmation message

            #sends email to user- set as backend to display in console during dev
            send_mail(
                'Reservation Cancelled',
                f'Your reservation on {reservation.date} at {reservation.time} has been successfully cancelled.',
                settings.DEFAULT_FROM_EMAIL,
                [request.user.email],
                fail_silently=False,
            )

            return redirect('reservation_list')  # Redirect to a list of reservations 
    else:
        form = CancelReservationForm(instance=reservation)
    
    return render(request, 'reservation/cancel_reservation.html', {'form': form, 'reservation': reservation})