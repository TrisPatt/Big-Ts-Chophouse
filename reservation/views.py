from django.shortcuts import render, redirect, get_object_or_404
from django.db import models
from .models import Reservation, Table, TimeSlot
from .forms import ReservationForm, CancelReservationForm
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Count, Sum
from django.contrib.auth.decorators import login_required
from datetime import date


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

def available_time_slots(request):
        selected_date = request.GET.get('date', date.today())
        all_time_slots = TimeSlot.objects.all()

         # Find booked time slots that are full (24 or more guests)
        booked_slots = Reservation.objects.filter(date=selected_date, reservation_status=0).values('time').annotate(total_guests=Sum('number_of_guests')).filter(total_guests__gte=24)

        # Exclude fully booked slots
        available_slots = all_time_slots.exclude(id__in=[slot['time'] for slot in booked_slots])

        return render(request, 'available_time_slots.html', {'available_slots': available_slots})

@login_required # Cancel reservations once logged in
def cancel_reservation(request, reservation_number):
    # Fetch the reservation based on the reservation_number and ensure the user is authorized
    reservation = get_object_or_404(Reservation, reservation_number=reservation_number, user_id=request.user)
    
    if request.method == 'POST':
        form = CancelReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            reservation.reservation_status = 1 #update status to cancelled
            form.save() 
            messages.success(request, 'Your reservation has been successfully cancelled.') 

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

@login_required
def update_reservation(request, reservation_number):
    try:
        # Fetch the reservation for the logged-in user
        reservation = Reservation.objects.get(reservation_number=reservation_number)
        print(f"Logged-in user: {request.user}")
        print(f"Reservation user: {reservation.user_id}")
    except Reservation.DoesNotExist:
        print("Reservation does not exist")
        raise

    # Ensure the reservation belongs to the logged-in user
    if reservation.user_id != request.user:
        print("Reservation does not belong to the logged-in user.")
        return redirect('reservation_list')

    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            updated_reservation = form.save(commit=False)
            updated_reservation.user_id = request.user

            num_guests = updated_reservation.number_of_guests
            tables_needed = (num_guests + 1) // 2  # Calculate tables needed

            # Check for table availability at the updated date and time, excluding current reservation
            total_guests_at_time = Reservation.objects.filter(
                date=updated_reservation.date,
                time=updated_reservation.time,
                reservation_status=0
            ).exclude(pk=reservation.pk).aggregate(total_guests=models.Sum('number_of_guests'))['total_guests'] or 0

            if total_guests_at_time + num_guests > 24:
                messages.error(request, "Sorry, we cannot accommodate your party size at the requested time.")
                return render(request, 'reservation/reservation_form.html', {'form': form, 'reservation': reservation})

            # Handle table assignment based on the update
            available_tables = Table.objects.annotate(
                reserved_count=models.Count('reservations', filter=models.Q(
                    reservations__date=updated_reservation.date,
                    reservations__time=updated_reservation.time,
                    reservations__reservation_status=0
                ))
            ).filter(reserved_count=0).count()

            if tables_needed <= available_tables:
                # Clear existing tables and assign new ones based on updated details
                updated_reservation.tables.clear()

                available_tables = Table.objects.annotate(
                    reserved_count=models.Count('reservations', filter=models.Q(
                        reservations__date=updated_reservation.date,
                        reservations__time=updated_reservation.time,
                        reservations__reservation_status=0
                    ))
                ).filter(reserved_count=0)[:tables_needed]

                updated_reservation.tables.add(*available_tables)
                updated_reservation.save()

                # Send a confirmation email for the updated reservation
                send_mail(
                    'Reservation Updated!',
                    f'Your reservation has been updated to {updated_reservation.date} at {updated_reservation.time}.',
                    settings.DEFAULT_FROM_EMAIL,
                    [request.user.email],
                    fail_silently=False,
                )

                messages.success(request, 'Your reservation has been successfully updated.')
                return redirect('reservation_confirmed', reservation_number=updated_reservation.pk)
            else:
                messages.error(request, "Sorry, not enough tables are available for your party size.")
                return render(request, 'reservation/reservation_form.html', {'form': form, 'reservation': reservation})
    else:
        form = ReservationForm(instance=reservation)

    return render(request, 'reservation/reservation_form.html', {'form': form, 'reservation': reservation})

    